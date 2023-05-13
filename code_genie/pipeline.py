import json
import os
import time
from typing import Any, Dict, List, Optional, TypeVar, Union

from pydantic import BaseModel, validator

from code_genie.genie import Genie, GenieResult
from code_genie.io import (
    BigQueryToDataframeSource,
    BoolArg,
    CsvToDataFrameSource,
    DataFrameToCsvSink,
    IntArg,
    StringArg,
)
from code_genie.io.argument import GenieArgument
from code_genie.io.base import GenieSource

Source = TypeVar("Source", CsvToDataFrameSource, BigQueryToDataframeSource)
Sink = TypeVar("Sink", bound=DataFrameToCsvSink)
Argument = TypeVar("Argument", StringArg, IntArg, BoolArg)


class PipelineStep(BaseModel):
    genie_result: GenieResult
    """Result of the genie which should be run in this step"""
    data: Optional[Union[Source, GenieResult]] = None
    """Data to be passed to the genie for computation. This could be either a data source or a previous genie result"""
    additional_inputs: Optional[Dict[str, Union[Source, GenieResult, Argument]]] = None
    """Set this value for each additional input to the genie. The dictionary key should be the name of the input
    and the value could be one of the 3 things: 
    1. A genie data source
    2. A genie result from a previous step
    3. A constant value to be passed as an argument to the pipeline"""
    sink: Optional[Sink] = None
    """If the output of this step needs to be exported, then a sink can be provided here"""


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
        """Add a step to the pipeline"""
        return self.copy(update={"steps": self.steps + [step]})

    @validator("steps")
    def _validate_steps(cls, v: List[PipelineStep]):
        # base_input of the first step should be a genie source
        if v[0].data is None:
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
        """Run the pipeline using the value of the arguments passed. Note that all arguments which do not have a
        default value needs to be passed here for the pipeline to run."""
        cached_genie_results: Dict[str, GenieResult] = {}
        for i, step in enumerate(self.steps):
            print(f"Running step {i+1}: {step.genie_result.id}")
            # initialize timer
            start_time = time.time()
            step_id = step.genie_result.id
            # get the base input
            if isinstance(step.data, GenieSource):
                base_input = step.data.get(**args)
            elif isinstance(step.data, GenieResult):
                base_input = self._get_cached_genie_result(
                    step_id=step_id, genie_id=step.data.id, cached_results=cached_genie_results
                )
            else:
                raise ValueError(f"Invalid type for base_input: {type(step.data)}")

            # get the additional inputs
            additional_inputs = {}
            for name, add_input in (step.additional_inputs or {}).items():
                if isinstance(add_input, GenieSource):
                    additional_inputs[name] = add_input.get(**args)
                if isinstance(add_input, GenieResult):
                    additional_inputs[name] = self._get_cached_genie_result(step_id, add_input.id, cached_genie_results)
                if isinstance(add_input, GenieArgument):
                    additional_inputs[name] = add_input.get(**args)

            # run the genie
            genie = Genie(data=base_input)
            genie_result = genie.run(step.genie_result.code, additional_inputs)
            cached_genie_results[step_id] = GenieResult(
                id=step_id, result=genie_result, code=step.genie_result.code, cache_dir=self.cache_dir
            )

            # write the output
            if step.sink is not None:
                step.sink.put(genie_result, **args)
            end_time = time.time()
            print(f"\tCompleted in {end_time - start_time:.1f} seconds")
