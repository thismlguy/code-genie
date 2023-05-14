from typing import Dict

import pandas as pd

from code_genie.io.argument import BoolArg, GenieArgument, StringArg
from code_genie.io.base import GenieSink, GenieSource


class DataFrameToCsvSink(GenieSink):
    path: StringArg
    """Path to the local file where data is to be exported."""
    index: BoolArg = BoolArg(name="export-pd-index", default_value=False)
    """Whether to export the index of the dataframe."""
    reset_index: BoolArg = BoolArg(name="reset-pd-index", default_value=True)
    """Whether to reset the index of the dataframe before exporting."""

    def put(self, data: pd.DataFrame, **kwargs):
        if self.reset_index.get(**kwargs):
            data = data.reset_index()
        data.to_csv(self.path.get(**kwargs), index=self.index.get(**kwargs))


class CsvToDataFrameSource(GenieSource):
    path: StringArg
    """Path to the local file from where data is to be imported from."""
    kwargs: Dict[str, GenieArgument] = {}
    """Any arguments to be passed to the pandas read_csv method."""

    def get(self, **kwargs):
        return pd.read_csv(self.path.get(**kwargs), **{k: v.get(**kwargs) for k, v in self.kwargs.items()})
