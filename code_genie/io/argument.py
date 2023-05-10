import os
import warnings
from abc import ABC
from typing import Any, Optional

from pydantic import BaseModel, validator


class GenieArgument(ABC, BaseModel):
    """Define an argument to the pipeline. This would be used to create the deployment setup"""

    name: str
    """Name of the argument, should only contain numbers, letters, dash and underscores; should start with a letter"""

    _value: Optional[Any] = None
    """Value of the argument; this will be set automatically by the pipeline object while running."""

    default_value: Optional[Any] = None  # set custom validator in the subclass
    """Default value of the argument if not provided"""

    env_var: Optional[str] = None
    """Name of the environment variable from which this argument should be read if not provided"""

    @validator("name")
    def name_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError(f"name must be a string, found: {v}")
        # check v contains only letters, numbers and underscores
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"name must only contain letters, numbers, dash and underscores, found: {v}")
        if not v[0].isalpha():
            raise ValueError(f"name must start with a letter, found: {v}")
        return v

    def get(self):
        """get the value of the argument using the following precedence:
        1. value set by the pipeline object
        2. env_var
        3. default_value
        """
        if self._value is not None:
            return self._value
        if self.env_var is not None:
            value = os.getenv(self.env_var)
            if value is None:
                warnings.warn(
                    f"No environment variable {self.env_var} found for argument: {self.name}"
                    f" falling back to default value"
                )
            else:
                return value
        if self.default_value is not None:
            return self.default_value
        raise ValueError(f"None of value or default_value or env_var provided for argument: {self.name}")


class StringArg(GenieArgument):
    @validator("default_value")
    def must_be_str(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError(f"default_value must be a string, found: {v}")
        return v


class IntArg(GenieArgument):
    @validator("default_value")
    def must_be_int(cls, v):
        if v is not None and not isinstance(v, int):
            raise ValueError(f"default_value must be an int, found: {v}")
        return v


class BoolArg(GenieArgument):
    @validator("default_value")
    def must_be_bool(cls, v):
        if v is not None and not isinstance(v, bool):
            raise ValueError(f"default_value must be a bool, found: {v}")
        return v
