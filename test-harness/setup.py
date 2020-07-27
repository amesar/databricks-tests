from setuptools import setup
  
setup(name='databricks-test-harness',
      version='0.0.1',
      description='databricks_test_harness',
      author='Andre',
      packages=[
        'databricks_test_server',
        'databricks_test_client'
        ],
      zip_safe=False,
      python_requires='>=3.6'
)

