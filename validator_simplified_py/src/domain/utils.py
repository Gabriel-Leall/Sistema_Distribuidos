import math
import time
from typing import List

class Utils:
    @staticmethod
    def calculate_standard_deviation(mrts: List[float]) -> float:
        """Calcula o desvio padrão dos MRTs."""
        # Calcula a soma
        total_sum = sum(mrts)
        
        # Calcula a média
        length = len(mrts)
        mean = total_sum / length
        
        # Calcula o desvio padrão
        standard_deviation = sum((num - mean) ** 2 for num in mrts)
        
        return math.sqrt(standard_deviation / length)

    @staticmethod
    def register_time(received_message: str) -> str:
        """Registra o tempo na mensagem recebida."""
        # Divide a mensagem e obtém o último timestamp
        string_splited = received_message.split(';')
        last_registered_time_stamp_string = string_splited[-1]
        
        # Obtém o tempo atual em milissegundos e calcula a diferença
        time_now = int(time.time() * 1000)
        time_diff = time_now - int(last_registered_time_stamp_string.strip())
        
        # Retorna a mensagem atualizada com os novos timestamps
        return f"{received_message}{time_now};{time_diff};" 