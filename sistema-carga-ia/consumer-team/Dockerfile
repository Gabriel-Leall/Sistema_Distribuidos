FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY consumer_team.py .

CMD ["python", "-u", "consumer_team.py"]