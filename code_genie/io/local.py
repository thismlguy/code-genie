from typing import Dict

import pandas as pd

from code_genie.io.argument import BoolArg, GenieArgument, StringArg
from code_genie.io.base import GenieSink, GenieSource


class DataFrameToCsvSink(GenieSink):
    path: StringArg
    index: BoolArg = BoolArg(name="export-pd-index", default_value=False)

    def put(self, data: pd.DataFrame):
        data.to_csv(self.path, index=self.index.get())


class CsvToDataFrameSource(GenieSource):
    path: StringArg
    kwargs: Dict[str, GenieArgument] = {}

    def get(self):
        return pd.read_csv(self.path, **{k: v.get() for k, v in self.kwargs.items()})
