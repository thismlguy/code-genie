from abc import ABC, abstractmethod
from typing import Union, List, Dict, Callable, Tuple, Optional

from code_genie.client import Client, GetExecutableRequest, GetPandasExecutableRequest


class GenieBase(ABC):

    def __init__(self,
                 instructions: Union[str, List[str]],
                 inputs: Dict[str, str],
                 allowed_imports: Optional[List[str]] = None,
                 client: Optional[Client] = None):
        self._inputs = inputs
        if isinstance(instructions, str):
            instructions = [instructions]
        self._instructions = instructions
        self._allowed_imports = allowed_imports
        self._code, self._fn_name = self._get_code(client=client or Client())
        self._executor = self._extract_executable(self._code, self._fn_name)

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
        return self._code


class Genie(GenieBase):

    def _get_code(self, client: Client) -> Tuple[str, str]:
        return client.get_generic(
            GetExecutableRequest(instructions=self._instructions,
                                 inputs=self._inputs,
                                 allowed_imports=self._allowed_imports))


class PandasGenie(GenieBase):

    def __init__(self,
                 instructions: Union[str, List[str]],
                 columns: Optional[List[str]] = None,
                 inputs: Optional[Dict[str, str]] = None,
                 allowed_imports: Optional[List[str]] = None,
                 client: Optional[Client] = None):
        self._columns = columns
        super().__init__(instructions, inputs, allowed_imports, client)

    def _get_code(self, client: Client) -> Tuple[str, str]:
        return client.get_pandas(
            GetPandasExecutableRequest(instructions=self._instructions,
                                       inputs=self._inputs,
                                       columns=self._columns,
                                       allowed_imports=self._allowed_imports))
