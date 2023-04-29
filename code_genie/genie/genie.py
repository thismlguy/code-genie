from typing import Tuple

from code_genie.client import Client, GetExecutableRequest
from code_genie.genie.base import GenieBase


class Genie(GenieBase):
    """A generic genie creator with no presets or additional functionality"""

    def _get_code(self, client: Client) -> Tuple[str, str]:
        return client.get_generic(
            GetExecutableRequest(
                instructions=self._instructions, inputs=self._inputs or {}, allowed_imports=self._allowed_imports
            )
        )
