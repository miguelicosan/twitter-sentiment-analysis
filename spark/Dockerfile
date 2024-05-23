FROM bitnami/spark:3.5.1

# Cambia al usuario root
USER root

# Crear directorios necesarios y establecer permisos
RUN mkdir -p /opt/bitnami/spark && chmod -R 777 /opt/bitnami/spark
RUN chmod -R 777 /tmp/

# Copiar el archivo requirements.txt y las dependencias Python
COPY ../requirements.txt /opt/bitnami/
RUN pip install --upgrade pip
RUN pip install -r /opt/bitnami/requirements.txt

# Crear un directorio para los datos de NLTK y establecer permisos
RUN mkdir -p /opt/bitnami/nltk_data && chmod -R 777 /opt/bitnami/nltk_data
ENV NLTK_DATA=/opt/bitnami/nltk_data

# Instalar textblob corpora
RUN python -m textblob.download_corpora

# Copiar el script de PySpark
COPY ./spark/transform_kafka_streaming.py /opt/bitnami/spark/transform_kafka_streaming.py

# Cambiar al usuario original
USER 1001

# Configurar Spark-submit para descargar los paquetes necesarios
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]

# elasticsearch-spark-30_2.12:8.13.4 -> Da un error de scala
# CMD ["spark-submit", "--master", "spark://spark-master:7077", "--packages", "org.elasticsearch:elasticsearch-spark-30_2.13:8.13.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "/opt/bitnami/spark/transform_kafka_streaming.py"]

# elasticsearch-spark-30_2.12:7.15.0 -> testing
CMD ["spark-submit", "--master", "spark://spark-master:7077", "--packages", "org.elasticsearch:elasticsearch-spark-30_2.12:7.15.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "/opt/bitnami/spark/transform_kafka_streaming.py"]