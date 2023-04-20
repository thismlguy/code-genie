from typing import Union, List, Dict, Callable

from code_genie.client import Client, GetExecutableRequest


class Genie:

    def __init__(self,
                 instructions: Union[str, List[str]],
                 inputs: Dict[str, str],
                 allowed_imports: List[str],
                 client: Client):
        self._inputs = inputs
        if isinstance(instructions, str):
            instructions = [instructions]
        self._instructions = instructions
        self._allowed_imports = allowed_imports
        self._code, self._fn_name = client.get_generic(
            GetExecutableRequest(instructions=instructions,
                                 inputs=inputs,
                                 allowed_imports=allowed_imports))
        self._executor = self._extract_executable(self._code, self._fn_name)

    @classmethod
    def _extract_executable(cls, code: str, fn_name: str) -> Callable:
        # define function in memory
        mem = {}
        exec(code, mem)
        return mem[fn_name]

    def __call__(self, **kwargs):
        return self._executor(**kwargs)

    @property
    def code(self):
        return self._code
