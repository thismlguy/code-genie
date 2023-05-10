from typing import Dict

import pandas as pd

from code_genie.io.argument import BoolArg, GenieArgument, StringArg
from code_genie.io.base import GenieSink, GenieSource


class DataFrameToCsvSink(GenieSink):
    path: StringArg
    index: BoolArg = BoolArg(name="export-pd-index", default_value=False)
    reset_index: BoolArg = BoolArg(name="reset-pd-index", default_value=True)

    def put(self, data: pd.DataFrame, **kwargs):
        if self.resolve_arg(self.reset_index, **kwargs):
            data = data.reset_index()
        data.to_csv(self.resolve_arg(self.path, **kwargs), index=self.resolve_arg(self.index, **kwargs))


class CsvToDataFrameSource(GenieSource):
    path: StringArg
    kwargs: Dict[str, GenieArgument] = {}

    def get(self, **kwargs):
        return pd.read_csv(
            self.resolve_arg(self.path, **kwargs), **{k: self.resolve_arg(v, **kwargs) for k, v in self.kwargs.items()}
        )
