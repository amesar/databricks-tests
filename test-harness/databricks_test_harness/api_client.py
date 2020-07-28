from databricks_cli.dbfs.api import DbfsApi, DbfsPath
from databricks_cli.runs.api import RunsApi
from databricks_cli.sdk import api_client
from databricks_test_harness import cred_utils

def get_api_client(profile=None):
    (host,token) = cred_utils.get_credentials(profile)
    print("Host:",host)
    return api_client.ApiClient(None, None, host, token)

class ApiClient():
    def __init__(self, profile=None):
        api_client =  get_api_client(profile)
        self.dbfs_client = DbfsApi(api_client)
        self.runs_client = RunsApi(api_client)

    def mkdirs(self, dbfs_path):
        return self.dbfs_client.mkdirs(DbfsPath(dbfs_path))

    def list_files(self, dbfs_path):
        return self.dbfs_client.list_files(DbfsPath(dbfs_path))

    def put_file(self, src_path, dbfs_path, overwrite=True):
        return self.dbfs_client.put_file(src_path, DbfsPath(dbfs_path), overwrite)

    def submit_run(self, json_data):
        return self.runs_client.submit_run(json_data)

    def get_run(self, run_id):
        return self.runs_client.get_run(run_id)
