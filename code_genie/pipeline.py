import json
import os
from typing import Dict, List, Optional, TypeVar

from pydantic import BaseModel, root_validator, validator

from code_genie.genie import GenieResult
from code_genie.io import BoolArg, CsvToDataFrameSource, DataFrameToCsvSink, IntArg, StringArg

# from code_genie.io.base import GenieSource, GenieSink

Source = TypeVar("Source", bound=CsvToDataFrameSource)
Sink = TypeVar("Sink", bound=DataFrameToCsvSink)
Argumnet = TypeVar("Argumnet", StringArg, IntArg, BoolArg)


class PipelineStep(BaseModel):
    genie_result: GenieResult
    """Result of the genie which should be run in this step"""
    base_input_source: Optional[Source] = None
    """Set this value if the base input to the genie should be read from a source"""
    base_input_genie: Optional[GenieResult] = None
    """Set this value if the base input to the genie should be read from a previous step"""
    additional_input_sources: Optional[Dict[str, Source]] = None
    """Set this value for each additional input to the genie which should be read from a source"""
    additional_input_genies: Optional[Dict[str, GenieResult]] = None
    """Set this value for each additional input to the genie which should be read from a previous step"""
    additional_input_arguments: Optional[Dict[str, Argumnet]] = None
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
            data = self.dict()
            json.dump(self.dict(), f)

    @classmethod
    def load(cls, filepath: str):
        """Load the pipeline from a json file"""
        with open(filepath, "r") as f:
            data = json.load(f)
            return cls.parse_obj(data)
