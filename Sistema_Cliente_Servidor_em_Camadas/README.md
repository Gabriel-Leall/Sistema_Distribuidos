# Sistema Cliente/Servidor em Camadas

## 📖 Descrição

Este projeto tem como objetivo implementar um sistema de processamento de imagens baseado em uma arquitetura de três camadas:

- **Cliente** – Interface gráfica desenvolvida com Tkinter, permitindo que o usuário envie imagens e visualize os resultados.
- **Servidor** – Desenvolvido em Flask, recebe as imagens via HTTP, aplica filtros e retorna as imagens processadas.
- **Banco de Dados** – Utiliza SQLite para armazenar os metadados das imagens (nome do arquivo, filtro aplicado e data/hora do processamento).

### Funcionamento

O sistema funciona da seguinte forma:

1. O cliente seleciona e envia uma imagem para o servidor via HTTP.
2. O servidor processa a imagem aplicando um filtro (como troca de cores).
3. A imagem modificada é enviada de volta ao cliente e exibida na interface gráfica.
4. Ambas as imagens (original e processada) são armazenadas no servidor.
5. Os metadados (nome do arquivo, filtro aplicado e data/hora) são registrados no banco de dados SQLite.
6. O cliente pode visualizar tanto a imagem original quanto a processada.

## 🗂️ Estrutura do Projeto

```
Sistema_Cliente_Servidor_em_Camadas/
|-- client/
|    |-- GUI.py
|-- server/
|    |-- database/
|        |-- init_db.sql
|        |-- metadados.db
|    |-- processed/
|    |-- uploads/
|    |-- app.py
|-- images/
```

### 🖥️ Client (Cliente)

📂 client/
Contém o código do cliente que envia imagens ao servidor e exibe os resultados processados.

- GUI.py → Interface gráfica desenvolvida com Tkinter.
    Permite que o usuário envie imagens.
    Escolhe um filtro.
    Recebe e exibe a imagem processada.

### 🌐 Server (Servidor)
📂 server/
Contém o código do servidor Flask, que recebe imagens do cliente, processa, armazena e retorna as imagens modificadas.

📂 database/ → Armazena o banco de dados do projeto.
  - init_db.sql → Script SQL para criar a estrutura inicial do banco.
  - metadados.db → Banco SQLite contendo informações sobre as imagens enviadas e processadas.

📂 processed/ → Diretório onde o servidor salva as imagens já processadas (modificadas).

📂 uploads/ → Diretório onde as imagens originais enviadas pelo cliente são armazenadas antes do processamento.

app.py → Código principal do servidor Flask.
- Recebe requisições do cliente (envio de imagens).
  - Salva as imagens em uploads/.
  - Aplica filtros e armazena o resultado em processed/.
  - Retorna ao cliente os caminhos das imagens para exibição.


