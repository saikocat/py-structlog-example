import sys
from random import random
from operator import add

from common.logging import structlogger
from common.logging.api import Logger
from common.signals_helper.shutdown_hook import register_shutdown_handler

from pyspark.sql import SparkSession


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark = SparkSession.builder.appName("PythonPi").getOrCreate()

    conf = spark.sparkContext.getConf()
    app_id = conf.get("spark.app.id")
    app_name = conf.get("spark.app.name")

    logger: Logger = structlogger.new_logger().bind(
        app_name=conf.get("spark.app.name"), app_id=conf.get("spark.app.id")
    )

    register_shutdown_handler(
        [
            lambda x, y: logger.warn(
                "app failed", department="infra", operation="ingest"
            ),
        ]
    )

    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = (
        spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    )
    logger.info("Pi is roughly %f" % (4.0 * count / n))
    logger.warn("Some partitions number", num_partitions=n, operation="ingest")

    spark.stop()
