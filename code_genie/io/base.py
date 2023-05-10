from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

from code_genie.io.argument import GenieArgument

ARG = TypeVar("ARG", bound=GenieArgument)


class GenieSource(ABC, BaseModel):
    @abstractmethod
    def get(self):
        raise NotImplemented


class GenieSink(ABC, BaseModel):
    @abstractmethod
    def put(self, data: Any):
        ...
