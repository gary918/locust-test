# Databricks notebook source
# MAGIC %md
# MAGIC ## Ingest Data from Azure Event Hubs

# COMMAND ----------

dbutils.widgets.text("CONNECTION_STR","")
# Read Event Hub's stream
conf = {}
conf["eventhubs.connectionString"] = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(dbutils.widgets.get("CONNECTION_STR"))

read_df = (
  spark
    .readStream
    .format("eventhubs")
    .options(**conf)
    .load()
)

# COMMAND ----------

# Read and transform
from pyspark.sql.types import *
import  pyspark.sql.functions as F
from pyspark.sql.functions import lit
from pyspark.sql.functions import col

read_schema = StructType([
           StructField('id', IntegerType(), True),
           StructField('amount', IntegerType(), True),
           StructField('ts', TimestampType(), True)
         ])
decoded_df = read_df.select(F.from_json(F.col("body").cast("string"), read_schema).alias("payload"))

decoded_df = decoded_df.select(col("payload.id"),col("payload.amount"),col("payload.ts"))
display(decoded_df)

# COMMAND ----------

checkpoint_path = f'/tmp/delta/flowers/checkpoints'
save_path = f'/tmp/delta/flowers'


decoded_df.writeStream \
  .format('delta') \
  .outputMode('append') \
  .option('checkpointLocation', checkpoint_path) \
  .start(save_path)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from delta.`/tmp/delta/flowers`

# COMMAND ----------

dbutils.fs.rm('/tmp/delta/flowers', True)
