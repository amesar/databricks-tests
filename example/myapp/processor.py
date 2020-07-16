from pyspark.sql.functions import col

def multiply(df, n):
    return df.withColumn("num", col("num") * n)
