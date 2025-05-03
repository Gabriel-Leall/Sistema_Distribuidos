# Usa uma imagem Python leve
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o script Python para o diretório de trabalho
COPY generator.py .

# Comando para executar o script quando o container iniciar
# O python -u garante que os prints apareçam imediatamente (unbuffered)
CMD ["python", "-u", "consumer_face.py"]