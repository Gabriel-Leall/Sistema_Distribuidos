# Sistema Cliente/Servidor com Threads

## 📖 Descrição

Este projeto implementa um sistema distribuído baseado em uma arquitetura cliente-servidor com múltiplos servidores escravos. O sistema é projetado para processar textos enviados pelo cliente, distribuindo as tarefas entre os servidores escravos e retornando os resultados ao cliente.

### Funcionamento

O sistema funciona da seguinte forma:

1. O cliente envia um texto para o servidor mestre via HTTP.
2. O servidor mestre distribui o texto para dois servidores escravos:
   - **Escravo 1**: Conta o número de letras no texto.
   - **Escravo 2**: Conta o número de números no texto.
3. Os servidores escravos processam o texto e retornam os resultados ao servidor mestre.
4. O servidor mestre combina os resultados e os envia de volta ao cliente.
5. O cliente exibe os resultados na interface gráfica.

## 🗂️ Estrutura do Projeto

```
cliente-servidor-threads/
|-- ClienteGUI.java
|-- docker-compose.yml
|-- Dockerfile.mestre
|-- Dockerfile.escravo1
|-- Dockerfile.escravo2
|-- servidores/
|    |-- ServidorMestre.java
|    |-- Escravo1.java
|    |-- Escravo2.java
```

### 🖥️ Cliente

📂 `ClienteGUI.java`  
Contém a interface gráfica do cliente, desenvolvida com **Swing**. Permite que o usuário envie textos para o servidor mestre e visualize os resultados.

- **Funcionalidades**:
  - Entrada de texto pelo usuário.
  - Envio do texto para o servidor mestre.
  - Exibição dos resultados retornados pelo servidor mestre.

### 🌐 Servidor Mestre

📂 `servidores/ServidorMestre.java`  
O servidor mestre recebe o texto do cliente, distribui as tarefas para os servidores escravos e retorna os resultados combinados ao cliente.

- **Funcionalidades**:
  - Recebe requisições HTTP do cliente.
  - Envia o texto para os servidores escravos.
  - Combina os resultados dos servidores escravos.
  - Retorna os resultados ao cliente.

### 🛠️ Servidores Escravos

📂 `servidores/Escravo1.java`  
📂 `servidores/Escravo2.java`  

Os servidores escravos processam o texto recebido do servidor mestre.

- **Escravo 1**:
  - Conta o número de letras no texto.
  - Retorna o resultado ao servidor mestre.

- **Escravo 2**:
  - Conta o número de números no texto.
  - Retorna o resultado ao servidor mestre.

### 🐳 Docker

O sistema utiliza **Docker** para facilitar a execução e o gerenciamento dos servidores.

- **Arquivos Docker**:
  - `Dockerfile.mestre`: Configura o servidor mestre.
  - `Dockerfile.escravo1`: Configura o servidor escravo 1.
  - `Dockerfile.escravo2`: Configura o servidor escravo 2.

- **docker-compose.yml**:
  - Define os serviços (mestre, escravo1, escravo2) e suas configurações.

## 📌 Guia de Instalação e Uso

### 1️⃣ Clonar o Repositório

```sh
git clone git@github.com:Gabriel-Leall/Sistema_Distribuidos.git
cd cliente-servidor-threads
```

### 2️⃣ Construir e Iniciar os Contêineres

📍 Use o **Docker Compose** para construir e iniciar os contêineres:

```sh
docker-compose up --build
```

Se tudo estiver correto, você verá mensagens indicando que o servidor mestre e os servidores escravos foram iniciados.

### 3️⃣ Rodar o Cliente

📍 Compile e execute o cliente:

```sh
javac ClienteGUI.java
java ClienteGUI
```

A interface gráfica será exibida, permitindo que você envie textos para o servidor.

### 4️⃣ Testar o Sistema

Na interface do cliente:

- Digite um texto no campo de entrada.
- Clique no botão "Enviar".
- O resultado será exibido no campo de saída, mostrando o número de letras e números no texto.

### 5️⃣ Parar os Contêineres

Para parar os contêineres, use:

```sh
docker-compose down
```

## 📂 Estrutura de Diretórios

```
cliente-servidor-threads/
|-- ClienteGUI.java         # Interface gráfica do cliente
|-- docker-compose.yml      # Configuração do Docker Compose
|-- Dockerfile.mestre       # Configuração do servidor mestre
|-- Dockerfile.escravo1     # Configuração do servidor escravo 1
|-- Dockerfile.escravo2     # Configuração do servidor escravo 2
|-- servidores/             # Código dos servidores
|    |-- ServidorMestre.java
|    |-- Escravo1.java
|    |-- Escravo2.java
```

## 🛠️ Tecnologias Utilizadas

- **Java**: Linguagem principal para o cliente e os servidores.
- **Swing**: Para a interface gráfica do cliente.
- **HttpServer**: Para implementar os servidores HTTP.
- **Docker**: Para containerização dos servidores.
- **Docker Compose**: Para orquestração dos contêineres.

## 📌 Observações

- Certifique-se de que o **Docker** e o **Docker Compose** estão instalados no sistema.
- O cliente deve ser executado localmente, enquanto os servidores são gerenciados via Docker.
