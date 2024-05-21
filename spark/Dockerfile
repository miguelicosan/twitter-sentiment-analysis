FROM bitnami/spark:latest

# Cambia al usuario root
USER root

# Crea el directorio y cambia los permisos
RUN mkdir -p /opt/bitnami/spark && chmod -R 777 /opt/bitnami/spark

# Copiar el archivo requirements.txt desde el directorio padre
COPY ../requirements.txt /opt/bitnami/

# Instalar las dependencias /opt/bitnami/
RUN pip install --upgrade pip
RUN pip install -r /opt/bitnami/requirements.txt

# Crear un directorio para los datos de NLTK y establecer permisos
RUN mkdir -p /opt/bitnami/nltk_data && chmod -R 777 /opt/bitnami/nltk_data

# Configurar la variable de entorno NLTK_DATA
ENV NLTK_DATA=/opt/bitnami/nltk_data

# Instalar textblob corpora
RUN python -m textblob.download_corpora

# Copiar el script de PySpark
COPY ./spark/transform_kafka_streaming.py /opt/bitnami/spark/transform_kafka_streaming.py

ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
CMD ["spark-submit", "--master", "spark://spark-master:7077", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1", "/opt/bitnami/spark/transform_kafka_streaming.py"]
