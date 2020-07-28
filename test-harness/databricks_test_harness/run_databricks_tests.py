import json, time
import click
from databricks_test_harness.api_client import ApiClient

@click.command()
@click.option("--json_spec_file", help="json spec file", required=True, type=str)
@click.option("--sleep_time", help="sleep time (seconds)", default=5, type=int)
@click.option("--open_browser", help="Open browser", default=False, type=bool)

def main(json_spec_file, sleep_time=5, open_browser=False):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")

    # Setup
    client = ApiClient()
    with open(json_spec_file, "r") as f:
        spec = json.loads(f.read())

    # Launch run
    res = client.submit_run(spec)
    print("submit_run result:",res)
    run_id = res["run_id"]
    print("run_id:",run_id)

    # Poll until run is finished
    cluster_id = None
    while True:
        res = client.get_run(run_id)
        state = res["state"]
        print("run_id:",run_id,"state:",state)
        cluster_instance = res.get("cluster_instance",None)
        if not cluster_id and cluster_instance:
            cluster_id = cluster_instance.get("cluster_id",None)
            print("cluster_id:",cluster_id)
        if state["life_cycle_state"] in ["TERMINATED","INTERNAL_ERROR" ]:
            break
        time.sleep(sleep_time)

    run_page_url = res["run_page_url"]
    print("cluster_id:",cluster_id)
    print("Run result:",run_page_url)
    if open_browser:
        import webbrowser
        webbrowser.open(run_page_url)

if __name__ == "__main__":
    main()
