import random
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Optional, Tuple, Callable, Any

from code_genie._cache import _CacheKey, _CacheValue
from code_genie.client import Client
from code_genie import CACHE


class GenieBase(ABC):

    def __init__(self,
                 instructions: Union[str, List[str]],
                 inputs: Optional[Dict[str, str]] = None,
                 allowed_imports: Optional[List[str]] = None,
                 override: bool = False,
                 client: Optional[Client] = None):
        """Initialize a genie instance

        Args:
            instructions: text instructions on the task required to be performed. use the keywords in inputs argument
                to refer to the inputs.
            inputs: a dictionary of inputs to the function. the keys are the names of the inputs and the values are
                small description of the inputs.
            allowed_imports: a list of imports which are allowed to be used in the code. note that this is not
                strictly enforced yet, but simplpy passed to the GPT API in the prompt.
            override: if a genie has been generated before with the same args, then it will be loaded from cache be
                default. set override to True to make a new API call and recreate the genie.
            client: an instance of the client to use for making requests to the api. if not provided, a new instance
                will be created.

        Returns:
            A callable which can be used to execute the code generated by the genie.
        """
        self._inputs = inputs
        if isinstance(instructions, str):
            instructions = [instructions]
        self._instructions = instructions
        self._allowed_imports = allowed_imports

        # check cache
        cache_key = self._get_hash_str()
        cache_value = CACHE.get(cache_key)
        if not override:
            if cache_value is not None:
                print(f"Loading executor from cache, set override = True to rerun")
                self._code = cache_value.code
                self._fn_name = cache_value.fn_name
                self._executor = self._extract_executable(self._code, self._fn_name)
                return
        # override or cache not found
        self._code, self._fn_name = self._get_code(client=client or Client())
        self._executor = self._extract_executable(self._code, self._fn_name)
        CACHE.update(cache_key,
                     self._get_cache_value(filename=cache_value.filename if cache_value else None))

    @abstractmethod
    def _get_code(self, client: Client) -> Tuple[str, str]:
        raise NotImplementedError

    @classmethod
    def _extract_executable(cls, code: str, fn_name: str) -> Callable:
        # define function in memory
        mem = {}
        exec(code, mem)
        return mem[fn_name]

    def __call__(self, *args, **kwargs):
        return self._executor(*args, **kwargs)

    @property
    def code(self):
        """The code generated by the genie"""
        return self._code

    def _instructions_hashable(self):
        return "::".join(self._instructions)

    def _input_hashable(self) -> Tuple[Tuple[str, str], ...]:
        return tuple(sorted((self._inputs or {}).items()))

    def _get_cache_key(self) -> _CacheKey:
        return _CacheKey(key=self.__class__.__name__,
                         instructions=self._instructions_hashable(),
                         inputs=self._input_hashable(),
                         allowed_imports=tuple(self._allowed_imports or []))

    @property
    def _export_filename(self) -> str:
        # use fn name with random 5 digit suffix
        return f"{self._fn_name}_{random.randint(10000, 99999)}.py"

    def _get_cache_value(self, filename: Optional[str]) -> _CacheValue:
        return _CacheValue(code=self._code, fn_name=self._fn_name, filename=filename or self._export_filename)

    def _hash_attributes(self) -> List[Any]:
        return [self._instructions, self._inputs, self._allowed_imports]

    def _get_hash_str(self) -> str:
        sep = "::"
        hash_str = []
        for attr in self._hash_attributes():
            # if string, add as is
            if isinstance(attr, str):
                hash_str.append(attr)
            # if list of str, then join using sep
            elif isinstance(attr, list):
                hash_str.append(sep.join(attr))
            # if dict, then convert to tuple of items
            elif isinstance(attr, dict):
                hash_str.append(sep.join([f"{k}={v}" for k, v in attr.items()]))
            # if None, return empty str
            elif attr is None:
                hash_str.append("")
            else:
                raise ValueError(f"Cannot hash attribute of type {type(attr)}")
        return sep.join(hash_str)
