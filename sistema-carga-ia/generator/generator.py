import pika
import time
import random
import json
import os
import sys

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
MESSAGES_PER_SECOND = 5 
EXCHANGE_NAME = 'image_topic_exchange'
ROUTING_KEYS = {
    'face': 'image.face',
    'team': 'image.team.crest'
}

def connect_rabbitmq():
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
    sys.exit(1) 

connection = connect_rabbitmq()
channel = connection.channel()
channel.confirm_delivery()  

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

print(f"Gerador pronto. Enviando {MESSAGES_PER_SECOND} mensagens por segundo para o exchange '{EXCHANGE_NAME}'...")

message_counter = 0
try:
    while True:
        message_type = random.choice(list(ROUTING_KEYS.keys())) 
        routing_key = ROUTING_KEYS[message_type]

        message_id = message_counter + 1
        message_body = {
            'id': message_id,
            'type': message_type,
            'data': f"simulated_{message_type}_data_{message_id}"
        }

        try:
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=routing_key,
                body=json.dumps(message_body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print(f" [✔] ACK recebido para '{routing_key}':'{message_body['id']} - {message_body['type']}'")
        except pika.exceptions.UnroutableError:
            print(f" [✖] Mensagem não roteável: '{routing_key}'")
        except Exception as e:
            print(f" [✖] Erro ao publicar: {e}")

        message_counter += 1
        time.sleep(1.0 / MESSAGES_PER_SECOND)

except KeyboardInterrupt:
    print("Interrompido pelo usuário.")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    if connection and connection.is_open:
        print("Fechando conexão com RabbitMQ.")
        connection.close()
