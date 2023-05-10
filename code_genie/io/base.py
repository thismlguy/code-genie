from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel

from code_genie.io.argument import GenieArgument

ARG = TypeVar("ARG", bound=GenieArgument)


class _Base(BaseModel):
    @classmethod
    def resolve_arg(cls, arg: GenieArgument, **kwargs):
        return arg.get(kwargs.get(arg.name))


class GenieSource(ABC, _Base):
    @abstractmethod
    def get(self, **kwargs):
        raise NotImplemented


class GenieSink(ABC, _Base):
    @abstractmethod
    def put(self, data: Any, **kwargs):
        ...
