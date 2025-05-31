import socket
import threading
import time
from typing import List, Tuple
from collections import deque
from .abstract_proxy import AbstractProxy

class LoadBalancerProxy(AbstractProxy):
    def __init__(self, porta_escuta: int, enderecos_servicos: List[Tuple[str, int]]):
        """
        Inicializa o balanceador de carga.
        
        Args:
            porta_escuta: Porta onde o balanceador irá escutar conexões
            enderecos_servicos: Lista de tuplas (ip, porta) dos serviços disponíveis
        """
        super().__init__()
        self.porta_escuta = porta_escuta
        self.enderecos_servicos = enderecos_servicos
        self.indice_atual = 0  # Para algoritmo round-robin

    def iniciar(self):
        """Inicia o balanceador de carga para escutar conexões."""
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            servidor.bind(('0.0.0.0', self.porta_escuta))
            servidor.listen()
            print(f"Balanceador de Carga escutando na porta {self.porta_escuta}")
            
            while True:
                socket_cliente, _ = servidor.accept()
                threading.Thread(
                    target=self.tratar_cliente,
                    args=(socket_cliente,),
                    daemon=True
                ).start()
        except Exception as e:
            print(f"Erro no Balanceador de Carga: {e}")
        finally:
            servidor.close()

    def tratar_cliente(self, socket_cliente: socket.socket):
        """
        Processa a requisição do cliente e redireciona para um serviço disponível.
        
        Args:
            socket_cliente: Socket conectado ao cliente
        """
        try:
            # Recebe dados do cliente
            dados = socket_cliente.recv(1024).decode()
            if not dados:
                return
                
            print(f"[BAL] Mensagem recebida do cliente: {dados}")

            # Adiciona timestamp de chegada
            dados = self.adicionar_timestamp_mensagem(dados)

            # Tenta encontrar um serviço livre (round-robin)
            for _ in range(len(self.enderecos_servicos)):
                ip, porta = self.enderecos_servicos[self.indice_atual]
                self.indice_atual = (self.indice_atual + 1) % len(self.enderecos_servicos)
                
                if self.servico_esta_livre(ip, porta):
                    print(f"Redirecionando para serviço: {ip}:{porta}")
                    
                    # Envia para o serviço e obtém resposta
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((ip, porta))
                        s.sendall(dados.encode())
                        resposta = s.recv(1024)
                    
                    # Adiciona timestamp de envio
                    resposta = self.adicionar_timestamp_resposta(resposta.decode())
                    socket_cliente.sendall(resposta.encode())
                    print(f"Resposta enviada ao cliente: {resposta}")
                    break
                else:
                    print(f"Serviço ocupado: {ip}:{porta}")
            else:
                # Todos os serviços ocupados
                print("Todos os serviços estão ocupados")
                socket_cliente.sendall("ocupado".encode())
                
        except Exception as e:
            print(f"Erro ao tratar cliente: {e}")
        finally:
            socket_cliente.close()

    def servico_esta_livre(self, ip: str, porta: int) -> bool:
        """
        Verifica se um serviço está disponível para receber requisições.
        
        Args:
            ip: Endereço IP do serviço
            porta: Porta do serviço
            
        Returns:
            True se o serviço está livre, False caso contrário
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)  # Timeout de 1 segundo
                s.connect((ip, porta))
                s.sendall("ping".encode())
                status = s.recv(1024).decode()
                return status.lower() == "livre"
        except Exception as e:
            print(f"Erro ao verificar serviço {ip}:{porta}: {e}")
            return False

    def adicionar_timestamp_mensagem(self, mensagem: str) -> str:
        """Adiciona timestamp à mensagem recebida."""
        tempo_atual = int(time.time() * 1000)
        return f"{mensagem};chegada:{tempo_atual};"

    def adicionar_timestamp_resposta(self, resposta: str) -> str:
        """Adiciona timestamp à resposta do serviço."""
        tempo_atual = int(time.time() * 1000)
        return f"{resposta};envio:{tempo_atual};"

if __name__ == "__main__":
    # Exemplo de uso
    servicos = [("localhost", 4001), ("localhost", 4002)]
    balanceador = LoadBalancerProxy(porta_escuta=2000, enderecos_servicos=servicos)
    balanceador.iniciar()