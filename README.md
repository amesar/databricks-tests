# databricks-tests

## Overview

* Example of wheel-based integration tests running as a Databricks job.
* This example outlines the steps that you need to integrate into your CI/CD test build.

## Run tests

```
cd example
```

**Setup**

Create a virtual environment and install `databricks-cli` PyPI package.
See [conda.yaml](example/conda.yaml).

```
conda env create conda.yaml
source activate databricks-tests-example
```

**Configure JSON run spec file**

Copy [run_submit.json.template](example/run_submit.json.template) and change `{BASE_DIR}` to point to your DBFS location.

```
sed -e "s;{BASE_DIR};dbfs:/jobs/myapp;" < run_submit.json.template > run_submit.json
```

**Copy test harness main program to DBFS**
```
databricks fs cp ../run_test.py dbfs:/jobs/myapp
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

