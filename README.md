# Sistema de Cadastro de Livros

## 📖 Descrição

Este projeto é um sistema de cadastro de livros para bibliotecas, permitindo a realização de operações de CRUD (Create, Read, Update e Delete). Essas operações correspondem, respectivamente, à criação, consulta, atualização e remoção de registros no banco de dados.

No sistema, são armazenadas as seguintes informações sobre os livros:

- **Título**
- **Autor**
- **Número de páginas**
- **Ano de publicação**
- **ID**

## ⚙️ Tecnologias Utilizadas

- **Python** – Linguagem de programação principal
- **PyQt5** – Para criação da interface gráfica
- **Firebase** – Para autenticação e armazenamento dos livros

## 🗂️ Estrutura do Projeto

```
biblioteca/
│── firebase/
│   │── config_firebase.py
│   │── livros.py
│── interface_grafica/
│   │── estilos.py
│   │── py/
│   │   │── add_livro.py
│   │   │── criar_conta.py
│   │   │── editar_livro.py
│   │   │── login.py
│   │   │── tela_inicial.py
│   │── ui/
│   │   │── add_livro.ui
│   │   │── criar_conta.ui
│   │   │── editar_livro.ui
│   │   │── login.ui
│   │   │── tela_inicial.ui
│── main_telas.py
```

### 📁 firebase/ (Gerenciamento do Firebase)

Aqui ficam os arquivos relacionados à conexão com o Firebase e operações no banco de dados.

- **config_firebase.py**: Configuração da conexão com o Firebase, incluindo autenticação e Firestore.
- **livros.py**: Contém as funções para manipular os dados dos livros no Firestore (adicionar, editar, excluir, listar, etc.).

### 📁 interface_grafica/ (Parte visual do sistema)

Essa pasta contém duas subpastas:

- **estilos.py** → Arquivo que centraliza as configurações de estilo para as interfaces gráficas.
- **py/** → Scripts Python que controlam as telas (lógica).
- **ui/** → Arquivos gerados pelo Qt Designer, contendo a estrutura das interfaces gráficas.

Cada tela tem um arquivo `.py` e um `.ui` correspondente:

- **add_livro.py/ui** → Tela para adicionar um novo livro.
- **criar_conta.py/ui** → Tela de cadastro de usuário.
- **editar_livro.py/ui** → Tela para editar informações de um livro existente.
- **login.py/ui** → Tela de login do sistema.
- **tela_inicial.py/ui** → Tela principal do sistema, onde o usuário navega.

Os arquivos `.ui` são criados no Qt Designer e precisam ser convertidos para `.py` com o comando:

```sh
pyuic5 -x interface_grafica/ui/tela_inicial.ui -o interface_grafica/py/tela_inicial.py
```

### 📄 main_telas.py (Arquivo principal)

Esse é o ponto de entrada do sistema. Ele:

- Inicializa o PyQt5.
- Gerencia a navegação entre as telas.
- Implementa a lógica de negócio do sistema.

---

## 📌 Guia de Instalação e Uso

### 1️⃣ Instalar Python 3.11.6

O Python 3.11.6 foi escolhido porque versões mais novas do Python (como 3.13) podem ter incompatibilidade com PyQt5, devido a mudanças internas na API do Python. Algumas versões mais antigas do PyQt5 podem não funcionar corretamente no Python 3.13, exigindo um downgrade para Python 3.11.6.

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

### **Inicialização do Pyrebase:**

```python
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
```

- Inicializa o Firebase com as configurações do firebaseConfig.
- Obtém uma instância de auth, usada para autenticação de usuários.

## 📱 Telas do Sistema

### Tela de Login

A Tela de Login é onde o usuário realiza a autenticação para acessar o sistema. Ela possui os seguintes componentes:

- Campos de entrada: Para o usuário inserir seu e-mail e senha.
- Botão de login: O usuário clica para autenticar e entrar no sistema.
- Botão de criação de conta: Caso o usuário ainda não tenha conta, ele pode clicar em "Criar Conta" para ser redirecionado para a tela de cadastro.
- Botão de sair: O sistema é encerrado.

Funções principais:

- Validar e autenticar o usuário no Firebase.
- Redirecionar para a Tela Inicial ou mostrar uma mensagem de erro.

<img src="https://github.com/user-attachments/assets/f132c494-6f1d-4e7e-8fcf-8f0eb20cdbc4" width="300" />

### Tela de Criar Conta

A Tela de Criar Conta permite que o usuário se registre no sistema. Ela contém os seguintes componentes:

- Campos de entrada: Para o usuário inserir seu e-mail, senha e confirmação da senha.
- Botão de cadastro: Ao clicar, o usuário será registrado no Firebase, e sua conta será criada.
- Botão de voltar: Para voltar à tela de login sem realizar o cadastro.

Funções principais:

- Criar uma nova conta de usuário no Firebase Authentication.
  Redirecionar para a Tela de Login caso o cadastro seja bem-sucedido.

<img src="https://github.com/user-attachments/assets/ee6f8132-7197-4e15-baf8-560d6c3f2333" width="300" />
<img src="https://github.com/user-attachments/assets/b87e185b-4147-483c-8b96-463797585f7e" width="300" />

### Tela Inicial

A Tela Inicial exibe a lista de livros cadastrados no sistema e contém as seguintes funcionalidades:

- Lista de livros: Exibe todos os livros já cadastrados com suas informações (por exemplo, título, autor, etc.).
- Campo de busca: Permite que o usuário pesquise um livro pelo ID. Se o livro for encontrado, ele aparecerá na lista com as opções de editar ou excluir.
- Botão de adicionar livro: Leva o usuário para a Tela de Adicionar Livro, permitindo que ele registre um novo livro no sistema.

Funções principais:

- Listar todos os livros cadastrados no sistema.
- Permitir buscar livros por ID.
- Redirecionar para a Tela de Adicionar Livro para inserir um novo livro.
- Permitir excluir livros existentes.
- Redirecionar para a Tela de Editar Livro para editar um livro existente.

<img src="https://github.com/user-attachments/assets/eac1181d-a9da-4609-a8e9-6344e04be0c2" width="600" />

### Tela de Adicionar Livro

A Tela de Adicionar Livro permite que o usuário cadastre um novo livro. Ela contém os seguintes campos:

- Campos de entrada: Para o usuário inserir informações do livro, como título, autor, ano de publicação, gênero, entre outros.
- Botão de salvar: Cadastra o novo livro no sistema.
- Botão de voltar: Permite voltar à tela inicial sem salvar o livro.

Funções principais:

- Coletar os dados do livro.
- Salvar o livro no Firebase Firestore.
- Redirecionar para a Tela Inicial após o cadastro bem-sucedido.

<img src="https://github.com/user-attachments/assets/92f9faea-5319-4d9e-9660-8ed5d5785bd6" width="400" />

### Tela de Editar Livro

A Tela de Editar Livro permite que o usuário edite as informações de um livro já cadastrado. Ela possui:

- Campos de entrada: Exibe as informações atuais do livro (título, autor, etc.), permitindo que o usuário edite esses dados.
- Botão de salvar: Salva as alterações no Firebase Firestore.
- Botão de cancelamento: Volta para a Tela Inicial sem salvar as modificações.

Funções principais:

- Exibir as informações do livro a ser editado.
- Permitir que o usuário altere os dados do livro.
- Atualizar o livro no Firebase Firestore.
- Redirecionar para a Tela Inicial após as alterações serem salvas.

<img src="https://github.com/user-attachments/assets/db63d202-f720-4bc6-a832-128e12c2267e" width="400" />

### 📧 Contato

Se houver dúvidas, sugestões ou desejo de colaboração no projeto, sinta-se à vontade para entrar em contato com os colaboradores.

erlanny.rego@ufpi.edu.br
gabrielleal7153@gmail.com
