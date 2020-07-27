import os
import importlib.resources as pkg_resources
import tempfile
import click
from databricks_test_client.api_client import ApiClient

_driver = "run_tests.py"

@click.command()
@click.option("--test_dir", help="DBFS test directory", required=True, type=str)
def main(test_dir):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    dst_path = os.path.join(test_dir,_driver)
    client = ApiClient()

    # Create DBFS test directory
    client.mkdirs(test_dir)

    # Copy test harness main program to DBFS
    file_content = pkg_resources.read_text(__package__, _driver)
    tmp_file = tempfile.NamedTemporaryFile(delete=True)
    print(f"tmp_file.name: {tmp_file.name}")
    try:
        tmp_file.write(bytes(file_content,"utf-8"))
        tmp_file.flush()
        client.put_file(tmp_file.name, dst_path)
    finally:
        tmp_file.close()  

    # List files in DBFS test directory
    files = client.list_files(test_dir)
    print(f"{dst_path}:")
    for file in files:
        print(f"  {file}")

if __name__ == "__main__":
    main()
