# databricks-tests

## Overview

* Example of wheel-based integration tests running as a Databricks job.
* This example outlines the steps that you need to integrate into your CI/CD test build.

There are two ways to run tests are demonstrated here:
* Manual - execute steps such as pushing files to DBFS, launching job and polling job in a manual fashion.
* Automated - Opinionated Python scripts to automate above steps with simple worfklow.

## Setup

**Databricks Workspace and Authentication**

Specifying your workspace and credentials is based on the Databricks CLI.
See [Set up authentication](https://docs.databricks.com/dev-tools/cli/index.html#set-up-authentication) in Databricks documentation.

**Conda environment**

Create a conda environment and install `databricks-cli` PyPI package.
See [conda.yaml](conda.yaml).

```
conda env create conda.yaml
source activate databricks-tests
```

**Configure JSON run spec file**

Copy [run_submit.json.template](example/run_submit.json.template) and change `{DBFS_DIR}` to point to your DBFS location.

```
cd example
sed -e "s;{DBFS_DIR};dbfs:/jobs/myapp;" < run_submit.json.template > run_submit.json
```

## Run Manual Tests

```
cd example
```

**Copy test harness main program to DBFS**

See [run_tests.py](test-harness/databricks_test_harness/run_tests.py).
```
databricks fs cp ../test-harness/databricks_test_harness/run_tests.py dbfs:/jobs/myapp --overwrite
```

**Build the wheel**
```
python setup.py bdist_wheel
```

**Copy the wheel to DBFS**
```
databricks fs cp dist/databricks_tests_example-0.0.1-py3-none-any.whl dbfs:/jobs/myapp
```

**Launch run to execute tests on Databricks cluster**

```
databricks runs submit --json-file run_submit.json
```
```
{
  "run_id": 2404336
}
```

**Poll the [run](https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-get) until it is in TERMINATED state**
```
databricks runs get --run-id 2404336
```

[PENDING state](example/samples/001_run_pending.json)
```
  "state": {
    "life_cycle_state": "PENDING",
    "state_message": "Waiting for cluster"
  },
```

[RUNNING state](example/samples/002_run_running.json)
```
  "state": {
    "life_cycle_state": "RUNNING",
    "state_message": "In run"
  },
```
[TERMINATED state](example/samples/003_run_terminated.json)
```
  "state": {
    "life_cycle_state": "TERMINATED",
    "result_state": "SUCCESS",
    "state_message": ""
  },
```

**Check the output logs**

Open up the `run_page_url` in your browser to view the logs in the Spark UI.

```
  "run_page_url": "https://demo.cloud.databricks.com#job/35950/run/1",
```

**Download the test results**

See [junit.xml](example/samples/junit.xml).
```
databricks fs cp dbfs:/jobs/myapp/junit.xml .
```
```
<?xml version="1.0" ?>
<testsuites>
  <testsuite
     errors="0"
     failures="0"
     hostname="0716-190309-boll22-10-0-249-156"
     name="pytest"
     skipped="0"
     tests="2"
     time="8.975"
     timestamp="2020-07-16T19:06:17.155587">
     <testcase classname="test_simple.TestSimple"
       file="../python3/lib/python3.7/site-packages/tests/test_simple.py"
       line="3"
       name="test_simple"
       time="0.001"/>
     <testcase classname="test_spark.TestSpark"
       file="../python3/lib/python3.7/site-packages/tests/test_spark.py"
       line="6"
       name="test_multiply"
       time="8.829"/>
  </testsuite>
</testsuites>
```

## Run Automated Tests

```
cd example
```

### Install
```
pip install -e ../test-harness
```

### Configure

This is a one-time initialization step.
The `configure` program does the following:
* Creates DBFS test directory
* Copies the test harness program [run_test.py](test-harness/databricks_test_harness/run_tests.py) to DBFS

```
python -m databricks_test_harness.configure  \
  --test_dir dbfs:/jobs/myapp 
```

### Build and push wheel to DBFS

```
python setup.py bdist_wheel
databricks fs cp dist/databricks_tests_example-0.0.1-py3-none-any.whl dbfs:/jobs/myapp --overwrite
```

### Run tests

Executes the [run_databricks_tests.py](run_databricks_tests.py) program which:
* Automates the individual API calls that comprise a test run
* Launches the test run
* Polls until the run is in TERMINATED or INTERNAL_ERROR state
* Downloads the junit.xml test results file
* Displays URI to driver logs

```
python -u -m databricks_test_harness.run_databricks_tests \
  --json_spec_file run_submit.json \
  --sleep_time 5
```

```
run_id: 2404423 state: {'life_cycle_state': 'PENDING', 'state_message': ''}
run_id: 2404423 state: {'life_cycle_state': 'PENDING', 'state_message': 'Waiting for cluster'}
cluster_id: 0727-174421-hag299
run_id: 2404423 state: {'life_cycle_state': 'PENDING', 'state_message': 'Waiting for cluster'}
. . .
run_id: 2404423 state: {'life_cycle_state': 'PENDING', 'state_message': 'Installing libraries'}
. . .
run_id: 2404423 state: {'life_cycle_state': 'RUNNING', 'state_message': 'In run'}
. . .
run_id: 2404423 state: {'life_cycle_state': 'TERMINATING', 'result_state': 'SUCCESS', 'state_message': 'Terminating the spark cluster'}
run_id: 2404423 state: {'life_cycle_state': 'TERMINATED', 'result_state': 'SUCCESS', 'state_message': ''}
Run results: https://demo.cloud.databricks.com#job/36040/run/1
```

### Check results
Check test results.
```
cat junit.xml
```

Check driver results.

Open `https://demo.cloud.databricks.com#job/36040/run/1` in your browser.

