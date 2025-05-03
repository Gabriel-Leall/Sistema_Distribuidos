import pika
import time
import json
import random
import os
import sys

# --- Configurações ---
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
EXCHANGE_NAME = 'image_topic_exchange'
QUEUE_NAME = 'team_identification_queue'
# Escuta por mensagens com routing key começando com 'image.team' (ex: image.team.crest, image.team.logo)
BINDING_KEY = 'image.team.#' # '#' casa com zero ou mais palavras separadas por '.'
PROCESSING_TIME_MIN = 0.6 # Tempo mínimo de processamento (em segundos)
PROCESSING_TIME_MAX = 1.8 # Tempo máximo de processamento (em segundos) - Também lento
# --------------------

def connect_rabbitmq():
    """Tenta conectar ao RabbitMQ com retries."""
    retries = 10
    while retries > 0:
        try:
            print(f"(Team Consumer) Tentando conectar ao RabbitMQ em {RABBITMQ_HOST}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
            )
            print("(Team Consumer) Conectado ao RabbitMQ!")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"(Team Consumer) Erro ao conectar: {e}. Tentando novamente em 5 segundos...")
            retries -= 1
            time.sleep(5)
    print("(Team Consumer) Não foi possível conectar ao RabbitMQ após várias tentativas.")
    sys.exit(1)

connection = connect_rabbitmq()
channel = connection.channel()

# Declara o exchange
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

# Declara a fila
result = channel.queue_declare(queue=QUEUE_NAME, durable=True, exclusive=False)
# queue_name = result.method.queue

print(f"(Team Consumer) Fila '{QUEUE_NAME}' declarada.")

# Vincula (bind) a fila ao exchange com a chave de roteamento wildcard
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=BINDING_KEY)

print(f"(Team Consumer) Fila '{QUEUE_NAME}' vinculada ao exchange '{EXCHANGE_NAME}' com a chave '{BINDING_KEY}'. Aguardando mensagens...")

# Lista de times de exemplo
TIMES_FUTEBOL = [
    "Corinthians", "Palmeiras", "São Paulo", "Santos", "Flamengo",
    "Vasco", "Fluminense", "Botafogo", "Grêmio", "Internacional",
    "Cruzeiro", "Atlético-MG"
]

def callback(ch, method, properties, body):
    """Função chamada quando uma mensagem é recebida."""
    message = json.loads(body.decode('utf-8'))
    message_id = message.get('id', 'N/A')
    message_data = message.get('data', 'N/A')

    print(f"\n(Team Consumer) [>] Recebido ID {message_id} (Routing Key: {method.routing_key}). Dados: {message_data}")

    # Simula o processamento da IA (mais lento que a geração)
    processing_time = random.uniform(PROCESSING_TIME_MIN, PROCESSING_TIME_MAX)
    print(f"(Team Consumer) [*] Processando brasão {message_id}... (simulando {processing_time:.2f}s)")
    time.sleep(processing_time)

    # Simula o resultado da IA
    time_identificado = random.choice(TIMES_FUTEBOL)
    confidence = random.uniform(0.75, 0.99)
    print(f"(Team Consumer) [<] Identificação de Time ID {message_id}: {time_identificado} (Confiança: {confidence:.2f})")

    # Confirma (ACK) o processamento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"(Team Consumer) [x] Mensagem {message_id} processada e ACK enviada.")

# Garante que o consumidor só receba a próxima mensagem após confirmar (ACK) a atual.
channel.basic_qos(prefetch_count=1)

# Inicia o consumo da fila
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback) # auto_ack=False

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n(Team Consumer) Interrompido pelo usuário.")
except Exception as e:
    print(f"(Team Consumer) Erro inesperado durante consumo: {e}")
finally:
    if connection and connection.is_open:
        print("(Team Consumer) Fechando conexão com RabbitMQ.")
        connection.close()