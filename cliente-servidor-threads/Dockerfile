# Usa imagem oficial do Java
FROM openjdk:21

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY ProjetoDistribuido /app/ProjetoDistribuido

# Expõe a porta que o servidor usa
EXPOSE 8000

# Comando para rodar o servidor
CMD ["java", "ProjetoDistribuido.ServidorMestre"]
