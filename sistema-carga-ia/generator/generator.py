import pika
import time
import random
import json
import os
import sys

# --- Configurações ---
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
MESSAGES_PER_SECOND = 5 # Taxa de geração de mensagens
EXCHANGE_NAME = 'image_topic_exchange'
ROUTING_KEYS = {
    'face': 'image.face',
    'team': 'image.team.crest'
}
# --------------------

def connect_rabbitmq():
    """Tenta conectar ao RabbitMQ com retries."""
    retries = 10
    while retries > 0:
        try:
            print(f"Tentando conectar ao RabbitMQ em {RABBITMQ_HOST}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
            )
            print("Conectado ao RabbitMQ!")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro ao conectar: {e}. Tentando novamente em 5 segundos...")
            retries -= 1
            time.sleep(5)
    print("Não foi possível conectar ao RabbitMQ após várias tentativas.")
    sys.exit(1) # Sai se não conseguir conectar

connection = connect_rabbitmq()
channel = connection.channel()

# Declara o exchange do tipo 'topic'
# Durable=True significa que o exchange sobreviverá a reinicializações do broker
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

print(f"Gerador pronto. Enviando {MESSAGES_PER_SECOND} mensagens por segundo para o exchange '{EXCHANGE_NAME}'...")

message_counter = 0
try:
    while True:
        message_type = random.choice(list(ROUTING_KEYS.keys())) # 'face' or 'team'
        routing_key = ROUTING_KEYS[message_type]

        message_id = message_counter + 1
        message_body = {
            'id': message_id,
            'type': message_type,
            # Simulando dados da imagem (poderia ser um path, URL ou até bytes)
            'data': f"simulated_{message_type}_data_{message_id}"
        }

        # Publica a mensagem no exchange com a routing key apropriada
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=json.dumps(message_body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Torna a mensagem persistente
            ))

        print(f" [x] Enviado '{routing_key}':'{message_body['id']} - {message_body['type']}'")
        message_counter += 1

        # Controla a taxa de envio
        time.sleep(1.0 / MESSAGES_PER_SECOND)

except KeyboardInterrupt:
    print("Interrompido pelo usuário.")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    if connection and connection.is_open:
        print("Fechando conexão com RabbitMQ.")
        connection.close()