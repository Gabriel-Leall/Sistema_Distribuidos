import socket
import threading
import time
from queue import Queue
from src.abstract_proxy import AbstractProxy
from src.service_ia import IA

class ServiceProxy(AbstractProxy):
    def __init__(self, porta_escuta: int, tempo_service_ms: float, tamanho_max_fila: int = 30, modelo_ai: str = "markov"):
        super().__init__()  
        self.porta_escuta = porta_escuta
        self.tempo_servico_ms = tempo_service_ms
        self.fila = Queue(maxsize=tamanho_max_fila) 
        self.tamanho_max_fila = tamanho_max_fila
        self.servico_ia = IA(modelo_ai=modelo_ai)

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            servidor.bind(('0.0.0.0', self.porta_escuta))
            servidor.listen()
            print(f"Serviço escutando na porta {self.porta_escuta}")
            
            while True:
                socket_cliente, _ = servidor.accept()
                threading.Thread(
                    target=self.tratar_cliente, 
                    args=(socket_cliente,),
                    daemon=True
                ).start()
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            servidor.close()

    def _extrair_ultimo_timestamp(self, mensagem: str) -> int:
        partes = mensagem.split(';')
        try:
            return int(partes[-2].strip()) if len(partes) >= 2 else 0
        except (ValueError, IndexError):
            return 0

    def adicionar_timestamp_mensagem_chega(self, mensagem: str) -> str:
        try:
            if not mensagem:
                return mensagem
            time_now = int(time.time() * 1000)
            ultimo_timestamp = self._extrair_ultimo_timestamp(mensagem)
            diferenca = time_now - ultimo_timestamp if ultimo_timestamp > 0 else 0
            return f"{mensagem}{time_now};{diferenca};"
        except Exception as e:
            print(f"Erro ao adicionar timestamp de chegada: {e}")
            return mensagem

    def adicionar_timestamp_mensagem_sai(self, mensagem: str) -> str:
        try:
            if not mensagem:
                return mensagem
            time_now = int(time.time() * 1000)
            partes = mensagem.split(';')
            if len(partes) >= 2:
                timestamp_chegada = int(partes[-2])
                tempo_processamento = time_now - timestamp_chegada
                return f"{mensagem}{time_now};{tempo_processamento};"
            return f"{mensagem}{time_now};0;"
        except Exception as e:
            print(f"Erro ao adicionar timestamp de saída: {e}")
            return mensagem

    def tratar_cliente(self, socket_cliente: socket.socket):
        try:
            dados = socket_cliente.recv(1024).decode()
            if not dados:
                return

            print(f"Mensagem recebida: {dados}")

            if dados == "ping":
                status = "ocupado" if self.fila.full() else "livre"
                ocupacao = self.fila.qsize() / self.tamanho_max_fila
                print(f"Status da fila: {status} ({ocupacao:.1%} de ocupação)")
                socket_cliente.sendall(status.encode())
                return

            if self.fila.full():
                print("Fila cheia - mensagem descartada")
                socket_cliente.sendall("ocupado".encode())
                return

            self.fila.put(dados)

            dados = self.adicionar_timestamp_mensagem_chega(dados)
            print(f"Processando com IA: {dados}")

            # processa com IA em vez de sleep
            resposta_ia = self.servico_ia.process(dados)

            resposta_ia = self.adicionar_timestamp_mensagem_sai(resposta_ia)
            print(f"Enviando resposta IA: {resposta_ia}")

            socket_cliente.sendall(resposta_ia.encode())

        except Exception as e:
            print(f"Erro ao tratar cliente: {e}")
        finally:
            socket_cliente.close()
