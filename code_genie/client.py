import os
from typing import Union, List, Dict, Tuple

import requests
from pydantic import BaseModel


class GetExecutableRequest(BaseModel):
    instructions: Union[str, List[str]]
    inputs: Dict[str, str]
    allowed_imports: List[str]


class GetExecutableResponse(BaseModel):
    executable: str
    fn_name: str


class Client:

    TOKEN_ENV_VAR = "CODE_GENIE_TOKEN"
    URL = "http://0.0.0.0"
    ENDPOINT_GENERIC = "get-executable"

    # def __init__(self):
    #     self._token = os.environ[self.TOKEN_ENV_VAR]

    def _get_response(self, endpoint, data):
        response = requests.put(url=f"{self.URL}/{endpoint}", data=data.json())
        return GetExecutableResponse.parse_obj(response.json())

    def get_generic(self, request: GetExecutableRequest) -> Tuple[str, str]:
        # send a request with given data
        response = self._get_response(self.ENDPOINT_GENERIC, request)
        return response.executable, response.fn_name
