from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, udf, date_format, lpad, concat
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import random

# Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("KafkaToDataFrame") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.9.3") \
    .getOrCreate()

# Función para convertir el día corto a largo
def convert_day(day):
    days = {
        'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday',
        'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'
    }
    return days.get(day, day)

def convert_month_long(month):
    months = {
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April', 'May': 'May', 'Jun': 'June',
        'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }
    return months.get(month, 'Unknown')

def get_sentiment(text):
    sentimientos = ["positive", "negative", "neutral"]
    return random.choice(sentimientos)

# UDFs para las conversiones y el análisis de sentimiento
convert_day_udf = udf(lambda x: convert_day(x), StringType())
convert_month_long_udf = udf(lambda x: convert_month_long(x), StringType())
sentiment_udf = udf(lambda x: get_sentiment(x), StringType())

# Leer datos desde Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9093,kafka3:9094") \
    .option("subscribe", "topic_tweets") \
    .option("startingOffsets", "latest") \
    .load()

# Seleccionar y convertir la columna "value" que contiene los mensajes
tweets = df.selectExpr("CAST(value AS STRING) as raw")
columnas = split(tweets['raw'], ',')
parsed_tweets = tweets.withColumn("label", columnas.getItem(0).cast("string")) \
    .withColumn("isa", columnas.getItem(1).cast("string")) \
    .withColumn("datelong", columnas.getItem(2).cast("string")) \
    .withColumn("flag", columnas.getItem(3).cast("string")) \
    .withColumn("user", columnas.getItem(4).cast("string")) \
    .withColumn("text", columnas.getItem(5).cast("string"))

parsed_tweets = parsed_tweets.withColumn("day_short", split(col("datelong"), ' ').getItem(0)) \
    .withColumn("month_short", split(col("datelong"), ' ').getItem(1)) \
    .withColumn("day_long", convert_day_udf(col("day_short"))) \
    .withColumn("month_long", convert_month_long_udf(col("month_short"))) \
    .withColumn("day", split(col("datelong"), ' ').getItem(2).cast(IntegerType())) \
    .withColumn("month", lpad(split(col("datelong"), ' ').getItem(1), 2, '0').cast(IntegerType())) \
    .withColumn("year", split(col("datelong"), ' ').getItem(5).cast(IntegerType())) \
    .withColumn("time", split(col("datelong"), ' ').getItem(3)) \
    .withColumn("hour", split(col("time"), ':').getItem(0).cast(IntegerType())) \
    .withColumn("minute", split(col("time"), ':').getItem(1).cast(IntegerType())) \
    .withColumn("second", split(col("time"), ':').getItem(2).cast(IntegerType())) \
    .withColumn("date", concat(col("year"), lpad(col("month"), 2, '0'), lpad(col("day"), 2, '0')))

parsed_tweets = parsed_tweets.withColumn("sentiment", sentiment_udf(col("text")))

# Escribir los datos procesados en la consola
console_query = parsed_tweets \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Escribir los datos procesados en Elasticsearch
es_query = parsed_tweets \
    .writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "elasticsearch") \
    .option("es.port", "9200") \
    .option("es.resource", "tweets/_doc") \
    .start()

# Agregar logging para confirmar la escritura en Elasticsearch
def process_row(row):
    logger.info(f"Processed row: {row}")

parsed_tweets.writeStream.foreach(process_row).start()

console_query.awaitTermination()
es_query.awaitTermination()
