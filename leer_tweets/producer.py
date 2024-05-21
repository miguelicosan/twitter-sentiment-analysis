import csv
import time
import random
import requests
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer

# Actualiza bootstrap_servers para incluir los tres brokers de Kafka
bootstrap_servers = ['kafka1:9092', 'kafka2:9093', 'kafka3:9094']
archivo_csv = '/data/tweets.csv'

def esperar_kafka():
    while True:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
            admin_client.list_topics()
            print('*********** KAFKA ESTÁ DISPONIBLE **************')
            return
        except Exception as e:
            print(':( :( :( :( :( :( :( :( :( :( :( Kafka no está disponible aún :( :( :( :( :( :( :( :( :( :( ')
            print(f'Error: {e}')
            time.sleep(5)

# def esperar_spark():
#     spark_master_url = "http://spark:8080"
#     while True:
#         try:
#             response = requests.get(spark_master_url)
#             if response.status_code == 200:
#                 print('*********** SPARK ESTÁ DISPONIBLE **************')
#                 return
#         except requests.ConnectionError as e:
#             print(':( :( :( :( :( :( :( :( :( :( :( Spark no está disponible aún :( :( :( :( :( :( :( :( :( :( ')
#             print(f'Error: {e}')
#             time.sleep(5)

def crear_topic_si_no_existe(topic_name):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    topics = admin_client.list_topics()
    topic_exists = any(topic_name == topic for topic in topics)
    if not topic_exists:
        new_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=3)  # Aquí se puede ajustar el número de particiones y réplicas
        admin_client.create_topics(new_topics=[new_topic], validate_only=False)
        print(f'Topic {topic_name} creado con éxito. :) :) :) :) :) :)')

def enviar_a_kafka(producer, topic_name, mensaje):
    producer.send(topic_name, mensaje.encode('utf-8'))
    producer.flush()
    print(f'Mensaje enviado al topic "{topic_name}": {mensaje}')

def leer_csv_y_enviar(topic_name):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    # Ajustando la lectura del archivo para manejar posibles errores de codificación
    try:
        with open(archivo_csv, mode='r', encoding='utf-8', errors='replace') as csvfile:
            total_filas = sum(1 for row in csvfile)
        with open(archivo_csv, mode='r', encoding='utf-8', errors='replace') as csvfile:
            reader = csv.reader(csvfile)
            while True:
                fila_aleatoria = random.randint(1, total_filas - 1)
                csvfile.seek(0)
                for i, fila in enumerate(reader):
                    if i == fila_aleatoria:
                        mensaje = ','.join(fila)
                        enviar_a_kafka(producer, topic_name, mensaje)
                        break
                time.sleep(5)
    except Exception as e:
        print(f'Error al leer el archivo CSV: {e}')
    producer.close()

esperar_kafka()
# esperar_spark()
topic_name = 'topic_tweets'
crear_topic_si_no_existe(topic_name)
leer_csv_y_enviar(topic_name)