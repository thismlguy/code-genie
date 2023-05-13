import os
import warnings
from abc import ABC
from typing import Any, Dict, Optional

from pydantic import BaseModel, root_validator, validator


class GenieArgument(ABC, BaseModel):
    """Define an argument to the pipeline. This would be used to create the deployment setup"""

    name: Optional[str] = None
    """Name of the argument, should only contain numbers, letters, dash and underscores; should start with a letter.
    If a name is provided, then the value of this argument can be set when running the script.
    If name is not provided, then default_value must be provided and the value of this argument cannot be set while 
    running the pipeline."""

    default_value: Optional[Any] = None  # set custom validator in the subclass
    """Default value of the argument if not provided"""

    env_var: Optional[str] = None
    """Name of the environment variable from which this argument should be read if not provided"""

    @validator("name")
    def name_valid(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError(f"name must be a string, found: {v}")
        # check v contains only letters, numbers and underscores
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"name must only contain letters, numbers, dash and underscores, found: {v}")
        if not v[0].isalpha():
            raise ValueError(f"name must start with a letter, found: {v}")
        return v

    @root_validator
    def name_or_default_value(cls, values):
        if "name" not in values and "default_value" not in values:
            raise ValueError("Either name or default_value must be provided, both are none")
        return values

    def get(self, **kwargs: Dict[str, "GenieArgument"]):
        """Resolve the value of the arg from the dictionary of arguments passed to the pipeline. Resolution is done
        using the following precedence:
        1. value set by the pipeline object
        2. env_var
        3. default_value
        """
        value = kwargs.get(self.name, None)
        if value is not None:
            return value
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
