import json
from datetime import datetime

class AbstractProxy:

    def __init__(self, log_file="log.json"):
        self.log_file = log_file
        self.init_log_file()

    def init_log_file(self):
        # Cria ou limpa o arquivo JSON com uma lista vazia
        with open(self.log_file, 'w') as f:
            json.dump([], f, indent=4)

    def log(self, message: str):
        print(message)  # Continua exibindo no console

        # Cria o registro com timestamp
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }

        # Lê os logs atuais
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        # Adiciona o novo log
        logs.append(log_entry)

        # Salva de volta no arquivo
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=4)
   