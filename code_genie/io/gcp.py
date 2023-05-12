from abc import ABC
from typing import Dict

from google.cloud import bigquery
from google.oauth2 import service_account

from code_genie.io.argument import GenieArgument, StringArg
from code_genie.io.base import GenieSource


class _WithCredentials(GenieSource, ABC):
    _default_key_path_env_var: str = "GOOGLE_APPLICATION_CREDENTIALS"

    key_path: StringArg = StringArg(env_var=_default_key_path_env_var)
    """Path to the GCP key file."""

    def _bq_client(self, **kwargs):
        credentials = service_account.Credentials.from_service_account_file(
            self.key_path.get(**kwargs),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return bigquery.Client(credentials=credentials, project=credentials.project_id)


class BigQueryToDataframeSource(_WithCredentials):
    query: str
    """Query to be used to read data from BQ"""
    query_args: Dict[str, GenieArgument]
    """Any arguments to be used in the query. These will be passed to the query using the format method."""

    def get(self, **kwargs):
        query = self.query
        if self.query_args:
            query = query.format(**{k: v.get(**kwargs) for k, v in self.query_args.items()})
        return self._bq_client(**kwargs).query(query).result().to_dataframe()
