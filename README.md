# Sistema de Cadastro de Livros

## Descrição
Este projeto é um sistema de cadastro de livros para bibliotecas, permitindo a realização de operações de CRUD (Create, Read, Update e Delete). Essas operações correspondem, respectivamente, à criação, consulta, atualização e remoção de registros no banco de dados.

No sistema, são armazenadas as seguintes informações sobre os livros:
- **Título**
- **Autor**
- **Número de páginas**
- **Ano de publicação**

## Tecnologias Utilizadas
- **Python** – Linguagem de programação principal
- **PyQt5** – Para criação da interface gráfica
- **Firebase** – Para autenticação e armazenamento dos livros

## Estrutura do Projeto
```
biblioteca/
│── firebase/
│   │── config_firebase.py
│   │── livros.py
│── interface_grafica/
│   │── py/
│   │   │__ add_livro.py
│   │   │-- criar_conta.py
│   │   │-- editar_livro.py
│   │   │-- login.py
│   │   │-- tela_inicial.py
│   │── ui/
│   │   │__ add_livro.ui
│   │   │-- criar_conta.ui
│   │   │-- editar_livro.ui
│   │   │-- login.ui
│   │   │-- tela_inicial.ui
│── main_telas.py
```

### 📁 firebase/ (Gerenciamento do Firebase)
Aqui ficam os arquivos relacionados à conexão com o Firebase e operações no banco de dados.

- **config_firebase.py**: Configuração da conexão com o Firebase, incluindo autenticação e Firestore.
- **livros.py**: Contém as funções para manipular os dados dos livros no Firestore (adicionar, editar, excluir, listar, etc.).

### 📁 interface_grafica/ (Parte visual do sistema)
Essa pasta contém duas subpastas:
- **py/** → Scripts Python que controlam as telas (lógica).
- **ui/** → Arquivos gerados pelo Qt Designer, contendo a estrutura das interfaces gráficas.

Cada tela tem um arquivo `.py` e um `.ui` correspondente:
- **add_livro.py** → Tela para adicionar um novo livro.
- **criar_conta.py** → Tela de cadastro de usuário.
- **editar_livro.py** → Tela para editar informações de um livro existente.
- **login.py** → Tela de login do sistema.
- **tela_inicial.py** → Tela principal do sistema, onde o usuário navega.

Os arquivos `.ui` são criados no Qt Designer e precisam ser convertidos para `.py` com o comando:
```sh
pyuic5 -x interface_grafica/ui/tela_inicial.ui -o interface_grafica/py/tela_inicial.py
```

### 📄 main_telas.py (Arquivo principal)
Esse é o ponto de entrada do sistema. Ele:
- Inicializa o PyQt5.
- Carrega a tela de login ou tela inicial.
- Gerencia a navegação entre as telas.

---

## 📌 Guia de Instalação e Uso

### 1️⃣ Instalar Python 3.11.6
O Python 3.11.6 foi escolhido porque versões mais novas podem ter incompatibilidade com PyQt5.

🔹 Baixe e instale o Python 3.11.6 em:
[Download Python 3.11.6](https://www.python.org/downloads/release/python-3116/)

### 2️⃣ Instalar as Bibliotecas
Para rodar o sistema, instale as dependências com:
```sh
pip install pyqt5 pyqt5-tools firebase_admin pyrebase
```
- **PyQt5**: Framework para criar interfaces gráficas em Python.
- **PyQt5-tools**: Ferramentas adicionais como o `designer.exe`.
- **firebase_admin**: SDK oficial do Firebase para Firestore e autenticação.
- **pyrebase**: Biblioteca para usar o Firebase Authentication e Storage.

### 3️⃣ Clonar o Repositório
```sh
git clone git@github.com:Gabriel-Leall/Sistema_Distribuidos.git
cd biblioteca
```

### 4️⃣ Configurar o Firebase
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Crie um novo projeto ou use um existente.
3. Vá em **Configurações do Projeto** → **Contas de Serviço** → **Gerar nova chave privada**.
4. Salve o arquivo `.json` na pasta `firebase/`.
5. No arquivo `firebase/config_firebase.py`, altere o caminho para seu JSON:
```python
cred = credentials.Certificate("firebase/seu-arquivo.json")
firebase_admin.initialize_app(cred)
```

### 5️⃣ Executar o Sistema
No terminal, dentro da pasta do projeto, rode:
```sh
python main_telas.py
```

---

## 🔥 Configuração do Firebase

### 🔹 Firebase Admin SDK
O arquivo `config_firebase.py` contém a configuração do Firebase Admin SDK.
#### Passos:
- **Carregar o arquivo JSON de credenciais**
- **Inicializar o Firebase Admin SDK**
```python
cred = credentials.Certificate("C:\\Users\\seu_usuario\\Documents\\Firebase\\seu-arquivo.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
```
- **Criar um cliente `db` para acessar o Firestore**

### 🔹 Configuração do Pyrebase
Além do Admin SDK, o projeto utiliza o Pyrebase para autenticação de usuários.

```python
firebaseConfig = {
  'apiKey': "SUA_API_KEY",
  'authDomain': "SEU_AUTH_DOMAIN",
  'projectId': "SEU_PROJECT_ID",
  'storageBucket': "SEU_STORAGE_BUCKET",  
  'messagingSenderId': "SEU_MESSAGING_SENDER_ID",
  'appId': "SEU_APP_ID",
  'measurementId': "SEU_MEASUREMENT_ID",
  'databaseURL': ""  
}
```
- Este dicionário contém as configurações públicas do Firebase usadas pelo Pyrebase.
- A chave databaseURL está vazia porque o Firestore é usado em vez do Realtime Database.

### 🔹 **Inicialização do Pyrebase:**
```python
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
```

- Inicializa o Firebase com as configurações do firebaseConfig.
- Obtém uma instância de auth, usada para autenticação de usuários.


