#!/bin/bash

# Comando para ejecutar spark-submit
spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.driver.extraClassPath=/opt/bitnami/spark/jars/* \
  --conf spark.executor.extraClassPath=/opt/bitnami/spark/jars/* \
  /opt/bitnami/spark/scripts/transform_kafka_streaming.py
