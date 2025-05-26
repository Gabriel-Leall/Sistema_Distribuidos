import socket
import time
import threading
from typing import List, Dict, Any
from .load_balancer_proxy import LoadBalancerProxy
from .utils import Utils

class Source:
    def __init__(self, load_balancer: LoadBalancerProxy):
        self.load_balancer = load_balancer
        self.source_current_index_message = 1
        self.arrival_delay = 2000  # 2 segundos
        self.model_feeding_stage = True  # Inicialmente definido como True
        self.dropp_count = 0
        self.connection_socket = None
        print("Source inicializado")

    def process_request(self, request: Dict[str, Any]):
        """
        Processa uma requisição de teste.
        
        Args:
            request: Dicionário contendo o tipo da requisição e a mensagem
        """
        msg = request.get("message", "")
        if not msg:
            return
            
        print(f"Processando requisição do tipo: {request.get('type', 'desconhecido')}")
        # Envia a mensagem para o balanceador de carga
        if self.is_destiny_free(self.load_balancer):
            self.send_message_to_destiny(msg)
        else:
            print(f"\n[DROPPED] Mensagem descartada em Source:")
            print(f"  - Tipo: {request.get('type', 'desconhecido')}")
            print(f"  - Mensagem: {msg.strip()}")
            print(f"  - Motivo: Balanceador ocupado")
            print(f"  - Total de mensagens descartadas: {self.dropp_count + 1}")
            self.dropp_count += 1

    def start(self):
        """Inicia o Source."""
        try:
            print("Iniciando Source...")
            # Conecta ao balanceador
            self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection_socket.connect(('localhost', self.load_balancer.local_port))
            print(f"Source conectado ao balanceador na porta {self.load_balancer.local_port}")
            
            # Inicia o balanceador
            self.load_balancer.start()
            
            time.sleep(0.1)
            print("Source iniciado")
            
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
            print(f"Enviando mensagem {self.source_current_index_message}")
            self.send(msg)
            self.source_current_index_message += 1
            time.sleep(self.arrival_delay / 1000)

    def send(self, msg: str):
        """Envia uma mensagem."""
        if self.is_destiny_free(self.load_balancer):
            self.send_message_to_destiny(msg)
        else:
            print(f"\n[DROPPED] Mensagem descartada em Source:")
            print(f"  - Mensagem: {msg.strip()}")
            print(f"  - Motivo: Balanceador ocupado")
            print(f"  - Total de mensagens descartadas: {self.dropp_count + 1}")
            self.dropp_count += 1
        time.sleep(self.arrival_delay / 1000)

    def send_message_to_destiny(self, msg: str):
        """Envia mensagem para o destino (LoadBalancer)."""
        try:
            self.connection_socket.send(msg.encode())
            print(f"Mensagem enviada para balanceador: {msg.strip()}")
        except Exception as e:
            print(f"Erro ao enviar mensagem para balanceador: {e}")

    def is_destiny_free(self, load_balancer: LoadBalancerProxy) -> bool:
        """Verifica se o destino está livre."""
        if not load_balancer or not self.connection_socket:
            return False
        try:
            self.connection_socket.send(b"ping")
            response = self.connection_socket.recv(1024).decode()
            return response == "free"
        except:
            return False 