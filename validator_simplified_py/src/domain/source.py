import socket
import time
import threading
from typing import List, Dict, Any
from .service_proxy import ServiceProxy
from .load_balancer_proxy import LoadBalancerProxy
from .utils import Utils

class Source:
    def __init__(self, service_proxy: ServiceProxy, load_balancer: LoadBalancerProxy):
        self.service_proxy = service_proxy
        self.load_balancer = load_balancer
        self.source_current_index_message = 1
        self.arrival_delay = 2000  # 2 segundos
        self.model_feeding_stage = True  # Inicialmente definido como True
        self.dropp_count = 0

    def process_request(self, request: Dict[str, Any]):
        """
        Processa uma requisição de teste.
        
        Args:
            request: Dicionário contendo o tipo da requisição e a mensagem
        """
        msg = request.get("message", "")
        if not msg:
            return
            
        # Envia a mensagem para o serviço apropriado
        if self.is_destiny_free(self.service_proxy.connection_destiny_socket):
            self.send_message_to_destiny(msg)
        else:
            print(f"\n[DROPPED] Mensagem descartada em Source:")
            print(f"  - Tipo: {request.get('type', 'desconhecido')}")
            print(f"  - Mensagem: {msg.strip()}")
            print(f"  - Motivo: Servico ocupado")
            print(f"  - Total de mensagens descartadas: {self.dropp_count + 1}")
            self.dropp_count += 1

    def start(self):
        """Inicia o Source."""
        try:
            # Inicia os proxies
            self.service_proxy.start()
            self.load_balancer.start()
            
            time.sleep(0.1)
            print("Starting source")
            
            if self.model_feeding_stage:
                self.send_message_feeding_stage()
                
        except Exception as e:
            print(f"Erro ao iniciar Source: {e}")

    def send_message_feeding_stage(self):
        """Envia mensagens na etapa de alimentação do modelo."""
        self.arrival_delay = 2000
        print("ATENCAO: Garanta que o atraso de chegada seja maior que a soma de todos os tempos de servico.")
        print("________________________________")
        print("Iniciando Etapa de Alimentacao do Modelo")
        print("________________________________")
        print(f"Apenas 10 requisicoes serao geradas com AD = {self.arrival_delay}ms")
        
        time.sleep(5)
        
        for j in range(10):
            msg = f"1;{self.source_current_index_message};{int(time.time() * 1000)};\n"
            self.send(msg)
            self.source_current_index_message += 1
            time.sleep(self.arrival_delay / 1000)

    def send(self, msg: str):
        """Envia uma mensagem."""
        if self.is_destiny_free(self.service_proxy.connection_destiny_socket):
            self.send_message_to_destiny(msg)
        else:
            print(f"\n[DROPPED] Mensagem descartada em Source:")
            print(f"  - Mensagem: {msg.strip()}")
            print(f"  - Motivo: Servico ocupado")
            print(f"  - Total de mensagens descartadas: {self.dropp_count + 1}")
            self.dropp_count += 1
        time.sleep(self.arrival_delay / 1000)

    def send_message_to_destiny(self, msg: str):
        """Envia mensagem para o destino."""
        try:
            self.service_proxy.connection_destiny_socket.send(msg.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem para destino: {e}")

    def is_destiny_free(self, socket_connection: socket.socket) -> bool:
        """Verifica se o destino está livre."""
        if not socket_connection:
            return False
        try:
            socket_connection.send(b"ping")
            response = socket_connection.recv(1024).decode()
            return response == "free"
        except:
            return False 