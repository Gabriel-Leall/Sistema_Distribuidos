import json
import os
from datetime import datetime


class AbstractProxy:
    def __init__(self, log_file="logs/log_source.json"):
        self.log_file = log_file

        # Cria a pasta, se não existir
        pasta = os.path.dirname(self.log_file)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)

    def log(self, message: str):
        print(message)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"[ERRO_LOG] {e} | Mensagem: {message}")
