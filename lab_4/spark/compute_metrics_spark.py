from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = (
        SparkSession.builder.master("spark://spark-master:7077")
        .appName("compute-metrics-spark")
        .getOrCreate()
    )

    numbers = [3, 7, 11, 19, 23]
    rows = [(value,) for value in numbers]
    df = spark.createDataFrame(rows, ["value"])

    result = df.agg(
        F.sum("value").alias("sum"),
        F.avg("value").alias("avg"),
        F.max("value").alias("max"),
    ).collect()[0]

    print(
        {
            "numbers": numbers,
            "count": len(numbers),
            "sum": result["sum"],
            "avg": result["avg"],
            "max": result["max"],
        }
    )

    spark.stop()


if __name__ == "__main__":
    main()
