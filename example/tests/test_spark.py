from pyspark.sql import SparkSession
import pytest
from myapp import processor

spark = SparkSession.builder.getOrCreate()

class TestSpark():
    def test_multiply(self):
        df = spark.createDataFrame([[1], [2], [3]], [ "num" ] )
        df = processor.multiply(df, 2)
        df2 = spark.createDataFrame([[2], [4], [6]], [ "num" ] )
        assert df.collect() == df2.collect()
