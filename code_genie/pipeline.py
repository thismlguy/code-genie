import json
import os
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, root_validator, validator

from code_genie.genie import Genie, GenieResult
from code_genie.io import BoolArg, CsvToDataFrameSource, DataFrameToCsvSink, IntArg, StringArg

Source = TypeVar("Source", bound=CsvToDataFrameSource)
Sink = TypeVar("Sink", bound=DataFrameToCsvSink)
Argument = TypeVar("Argument", StringArg, IntArg, BoolArg)


class PipelineStep(BaseModel):
    genie_result: GenieResult
    """Result of the genie which should be run in this step"""
    base_input_source: Optional[Source] = None
    """Set this value if the base input to the genie should be read from a source"""
    base_input_genie: Optional[GenieResult] = None
    """Set this value if the base input to the genie should be read from a previous step; If a genie is set here, then
    the genie should have been run in a previous step in the pipeline"""
    additional_input_sources: Optional[Dict[str, Source]] = None
    """Set this value for each additional input to the genie which should be read from a source"""
    additional_input_genies: Optional[Dict[str, GenieResult]] = None
    """Set this value for each additional input to the genie which should be read from a previous step"""
    additional_input_arguments: Optional[List[Argument]] = None
    """Set this value for each additional input to the genie which should be read from a constant value passed as an
    argument to the pipeline"""
    sink: Optional[Sink] = None
    """If the output of this step needs to be exported, then a sink can be provided here"""

    # validate either one of base_input_source or base_input_genie should be set
    @root_validator()
    def _validate_base_input(cls, values):
        if values.get("base_input_source") is None and values.get("base_input_genie") is None:
            raise ValueError("Either base_input_source or base_input_genie should be set")
        return values


class GeniePipeline(BaseModel):
    name: str
    """Name of the pipeline"""
    version: str
    """Version of the pipeline"""
    cache_dir: str
    """Directory where the genies being used in this pipeline are cached. The pipeline will also be cached at the 
    same location"""
    steps: List[PipelineStep]
    """List of steps in the pipeline"""

    def add(self, step: PipelineStep):
        return self.copy(update={"steps": self.steps + [step]})

    @validator("steps")
    def _validate_steps(cls, v: List[PipelineStep]):
        # base_input of the first step should be a genie source
        if v[0].base_input_source is None:
            raise ValueError(f"base_input_source of the first step should be set, found None")
        # there should be atleast 1 sink
        if all(step.sink is None for step in v):
            raise ValueError("atleast one of the steps should have a sink; none found")
        return v

    def _get_filepath(self, filename: str):
        if not filename.endswith("json"):
            filename += ".json"
        return os.path.join(self.cache_dir, filename)

    def export(self, filename: str):
        """Export the pipeline as a json file"""
        with open(self._get_filepath(filename), "w") as f:
            json.dump(self.dict(), f)

    @classmethod
    def load(cls, filepath: str):
        """Load the pipeline from a json file"""
        with open(filepath, "r") as f:
            return cls.parse_obj(json.load(f))

    @classmethod
    def _get_cached_genie_result(cls, step_id: str, genie_id: str, cached_results: Dict[str, GenieResult]):
        if genie_id not in cached_results:
            raise ValueError(
                f"Error in step id id: {step_id}; You are attempting to use the results of genie with id: {genie_id} "
                f"in this step but the genie has not been run in a previous step. Add a step before this step in the "
                f"pipeline to run genie id {genie_id}."
            )
        return cached_results[genie_id].result

    def run(self, args: Dict[str, Any]):
        """Run the pipeline"""
        cached_genie_results: Dict[str, GenieResult] = {}
        for i, step in enumerate(self.steps):
            step_id = step.genie_result.id
            # get the base input
            if step.base_input_source is not None:
                base_input = step.base_input_source.get(**args)
            else:
                base_input = self._get_cached_genie_result(
                    step_id=step_id, genie_id=step.base_input_genie.id, cached_results=cached_genie_results
                )

            # get the additional inputs
            additional_inputs = {}
            for name, source in (step.additional_input_sources or {}).items():
                additional_inputs[name] = source.get(**args)
            for name, genie in (step.additional_input_genies or {}).items():
                additional_inputs[name] = self._get_cached_genie_result(step_id, genie.id, cached_genie_results)
            for argument in step.additional_input_arguments or []:
                additional_inputs[argument.name] = argument.get(args.get(argument.name))

            # run the genie
            genie = Genie(data=base_input)
            genie_result = genie.run(step.genie_result.code, additional_inputs)
            cached_genie_results[step_id] = GenieResult(
                id=step_id, result=genie_result, code=step.genie_result.code, cache_dir=self.cache_dir
            )

            # write the output
            if step.sink is not None:
                step.sink.put(genie_result, **args)
