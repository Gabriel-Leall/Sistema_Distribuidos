# 🧠🔁 Sistema Distribuído com IA Simulada via RabbitMQ

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-orange?logo=rabbitmq)](https://www.rabbitmq.com/)

Um sistema assíncrono e escalável que simula o processamento de imagens com **IA embarcada** usando **RabbitMQ** e **Docker**.

## 📸 Visão Geral

Este projeto implementa uma arquitetura **event-driven** com múltiplos consumidores especializados:

- 🎛 **Gerador** de mensagens (imagens faciais e brasões)
- 🤖 **IA 1**: Detecta o **sentimento facial**
- 🏆 **IA 2**: Reconhece o **time de futebol**
- 🐇 **Broker RabbitMQ** para entrega e roteamento

## 📂 Estrutura do Projeto

```
.
├── docker-compose.yml
├── requirements.txt
├── generator/
|   ├── Dockerfile
│   └── generator.py
├── consumer-face/
|   ├── Dockerfile
│   └── consumer_face.py
├── consumer-team/
|   ├── Dockerfile
│   └── consumer_team.py
└── README.md
```

## 🔧 Tecnologias Usadas

- Python 3.10+
- RabbitMQ (topic exchange)
- Docker e Docker Compose
- Biblioteca `pika` para comunicação AMQP

## 🚀 Como Executar

### 1. Clone o repositório

```
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Instale as dependências
```
pip install -r requirements.txt
```

### 3. Construa e inicie os containers

```
docker-compose up --build
```

### 4. Acesse a interface de gerenciamento do RabbitMQ

- URL: http://localhost:15672
- Usuário: guest
- Senha: guest

## 🔄 Fluxo das Mensagens

1. O generator envia mensagens para o exchange image_topic_exchange com routing keys como:
- image.face
- image.team.crest

2. O exchange (do tipo topic) distribui as mensagens:
- consumer_face recebe mensagens image.face
- consumer_team recebe mensagens image.team.

3. Cada consumidor simula uma análise com IA:
- Rosto → Sentimento
- Time → Identificação do clube com confiança

## 🕵️‍♂️ Monitoramento
- Os consumidores são mais lentos que o gerador (intencionalmente), então a fila cresce ao longo do tempo.
- Você pode observar o crescimento e o esvaziamento das filas via interface do RabbitMQ.

![Painel do RabbitMQ](images/rabbitmq_dashboard.png)

