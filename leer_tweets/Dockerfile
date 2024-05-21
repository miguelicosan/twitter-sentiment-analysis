FROM python:3.10.12-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia los scripts y datos necesarios
COPY ./leer_tweets/producer.py /app/producer.py
COPY ./data/tweets.csv /data/tweets.csv

# Comando para ejecutar el script
CMD ["python", "-u", "producer.py"]
