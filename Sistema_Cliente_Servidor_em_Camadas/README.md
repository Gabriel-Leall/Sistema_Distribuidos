# Sistema Cliente/Servidor em Camadas

## 📖 Descrição

Este projeto tem como objetivo implementar um sistema de processamento de imagens baseado em uma arquitetura de três camadas:

- Cliente – Interface gráfica desenvolvida com Tkinter, permitindo que o usuário envie imagens e visualize os resultados.
- Servidor – Desenvolvido em Flask, recebe as imagens via HTTP, aplica filtros e retorna as imagens processadas.
- Banco de Dados – Utiliza SQLite para armazenar os metadados das imagens (nome do arquivo, filtro aplicado e data/hora do processamento).
