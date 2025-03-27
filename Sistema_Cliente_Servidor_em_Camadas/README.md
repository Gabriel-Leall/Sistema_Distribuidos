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
|    |-- processed/
|    |-- uploads/
|    |-- app.py
|-- images/
```
