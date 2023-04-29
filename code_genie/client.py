import os
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

import requests
from pydantic import BaseModel


class GetExecutableRequest(BaseModel):
    instructions: Union[str, List[str]]
    inputs: Dict[str, str]
    allowed_imports: Optional[List[str]] = None


class GetPandasExecutableRequest(GetExecutableRequest):
    inputs: Optional[Dict[str, str]] = None
    columns: Optional[List[str]] = None


class GetExecutableResponse(BaseModel):
    id: UUID
    code: str
    fn_name: str


class Client:
    TOKEN_ENV_VAR = "CODE_GENIE_TOKEN"
    URL = "https://code-scribe-pzj44qvhfa-el.a.run.app"
    ENDPOINT_GENERIC = "get-executable/generic"
    ENDPOINT_PANDAS = "get-executable/pandas"

    def __init__(self, token: Optional[str] = None):
        self._token = token or os.environ[self.TOKEN_ENV_VAR]

    def _get_response(self, endpoint, data):
        headers = {"token": self._token, "Content-Type": "application/json"}
        response = requests.post(url=f"{self.URL}/{endpoint}", data=data.json(), headers=headers)
        # if error found, raise the error
        response.raise_for_status()
        return GetExecutableResponse.parse_obj(response.json())

    def get_generic(self, request: GetExecutableRequest) -> Tuple[str, str]:
        # send a request with given data
        response = self._get_response(self.ENDPOINT_GENERIC, request)
        return response.code, response.fn_name

    def get_pandas(self, request: GetPandasExecutableRequest) -> Tuple[str, str]:
        # send a request with given data
        response = self._get_response(self.ENDPOINT_PANDAS, request)
        return response.code, response.fn_name
