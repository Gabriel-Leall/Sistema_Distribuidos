import pika
import time
import json
import random
import os
import sys

# --- Configurações ---
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
EXCHANGE_NAME = 'image_topic_exchange'
QUEUE_NAME = 'face_analysis_queue'
BINDING_KEY = 'image.face' # Escuta por mensagens com routing key começando com 'image.face'
PROCESSING_TIME_MIN = 0.5 # Tempo mínimo de processamento (em segundos)
PROCESSING_TIME_MAX = 1.5 # Tempo máximo de processamento (em segundos) - Mais lento que o gerador
# --------------------

def connect_rabbitmq():
    """Tenta conectar ao RabbitMQ com retries."""
    retries = 10
    while retries > 0:
        try:
            print(f"(Face Consumer) Tentando conectar ao RabbitMQ em {RABBITMQ_HOST}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
            )
            print("(Face Consumer) Conectado ao RabbitMQ!")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"(Face Consumer) Erro ao conectar: {e}. Tentando novamente em 5 segundos...")
            retries -= 1
            time.sleep(5)
    print("(Face Consumer) Não foi possível conectar ao RabbitMQ após várias tentativas.")
    sys.exit(1)

connection = connect_rabbitmq()
channel = connection.channel()

# Declara o exchange (deve ser o mesmo tipo e nome do gerador)
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

# Declara a fila (durable=True para sobreviver a reinicializações)
# exclusive=False permite que multiplas instâncias do consumidor (se necessário) usem a mesma fila
result = channel.queue_declare(queue=QUEUE_NAME, durable=True, exclusive=False)
# queue_name = result.method.queue # Não precisamos mais disso se especificamos o nome

print(f"(Face Consumer) Fila '{QUEUE_NAME}' declarada.")

# Vincula (bind) a fila ao exchange com a chave de roteamento específica
channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=BINDING_KEY)

print(f"(Face Consumer) Fila '{QUEUE_NAME}' vinculada ao exchange '{EXCHANGE_NAME}' com a chave '{BINDING_KEY}'. Aguardando mensagens...")

def callback(ch, method, properties, body):
    """Função chamada quando uma mensagem é recebida."""
    message = json.loads(body.decode('utf-8'))
    message_id = message.get('id', 'N/A')
    message_data = message.get('data', 'N/A')

    print(f"\n(Face Consumer) [>] Recebido ID {message_id} (Routing Key: {method.routing_key}). Dados: {message_data}")

    # Simula o processamento da IA (mais lento que a geração)
    processing_time = random.uniform(PROCESSING_TIME_MIN, PROCESSING_TIME_MAX)
    print(f"(Face Consumer) [*] Processando rosto {message_id}... (simulando {processing_time:.2f}s)")
    time.sleep(processing_time)

    # Simula o resultado da IA
    sentimento = random.choice(['Feliz', 'Triste', 'Neutro', 'Surpreso'])
    print(f"(Face Consumer) [<] Análise de Sentimento ID {message_id}: {sentimento}")

    # Confirma (ACK) o processamento da mensagem para removê-la da fila
    # Isso é crucial para garantir que a mensagem não seja reprocessada em caso de falha
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"(Face Consumer) [x] Mensagem {message_id} processada e ACK enviada.")

# Garante que o consumidor só receba a próxima mensagem após confirmar (ACK) a atual.
# Importante para evitar sobrecarga e garantir processamento em ordem (por consumidor).
channel.basic_qos(prefetch_count=1)

# Inicia o consumo da fila, chamando a função 'callback' para cada mensagem
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback) # auto_ack=False é o padrão e o correto aqui

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\n(Face Consumer) Interrompido pelo usuário.")
except Exception as e:
    print(f"(Face Consumer) Erro inesperado durante consumo: {e}")
finally:
     if connection and connection.is_open:
        print("(Face Consumer) Fechando conexão com RabbitMQ.")
        connection.close()