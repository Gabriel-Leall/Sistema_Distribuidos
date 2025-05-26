import socket
import random
import time
from typing import List, Dict
from collections import deque
from .abstract_proxy import AbstractProxy
from .target_address import TargetAddress

class LoadBalancerProxy(AbstractProxy):
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.proxy_name = config['name']
        self.local_port = config['port']
        self.current_target_index = 0
        self.num_services = config['num_services']
        self.queue = deque(maxlen=config['queue_size'])
        self.service_time = config['service_time']
        self.std = config['std']
        self.is_source = config['is_source']
        
        # Criar lista de serviços
        self.targets = self._create_services()
        self.connection_destiny_sockets = []

    def _create_services(self) -> List[TargetAddress]:
        """Cria a lista de serviços baseada na configuração."""
        services = []
        for i in range(self.num_services):
            service = TargetAddress(
                host='localhost',
                port=self.config['port'] + i + 1,
                service_time=self.service_time,
                std=self.std
            )
            services.append(service)
        return services

    def _handle_origin_connection(self):
        """Lida com a conexão de origem."""
        try:
            while self.is_running:
                data = self.connection_origin_socket.recv(1024).decode()
                if not data:
                    break
                
                if data.strip() == "ping":
                    self._handle_ping_message(self.connection_origin_socket)
                elif data.startswith("config;"):
                    self._handle_config_message(data)
                else:
                    self._handle_message(data)
                    
        except Exception as e:
            print(f"Erro ao lidar com conexão de origem: {e}")
        finally:
            if self.connection_origin_socket:
                try:
                    self.connection_origin_socket.close()
                except:
                    pass

    def _handle_destiny_connection(self):
        """Lida com a conexão de destino."""
        try:
            while self.is_running:
                data = self.connection_destiny_socket.recv(1024).decode()
                if not data:
                    break
                
                # Verifica se é uma mensagem de ping
                if data.strip() == "ping":
                    self._handle_ping_message(self.connection_destiny_socket)
                    continue
                
                # Registra o tempo quando a mensagem chega
                data = self._register_time_when_arrives(data)
                
                # Simula o processamento
                time.sleep(0.1)  # Simula processamento
                
                # Registra o tempo quando a mensagem sai
                data = self._register_time_when_goes_out(data)
                
                # Envia a mensagem de volta para a origem
                if self.connection_origin_socket:
                    try:
                        self.connection_origin_socket.send(data.encode())
                    except:
                        print("Erro ao enviar resposta para origem")
                
        except Exception as e:
            print(f"Erro ao lidar com conexão de destino: {e}")
        finally:
            if self.connection_destiny_socket:
                try:
                    self.connection_destiny_socket.close()
                except:
                    pass

    def _handle_config_message(self, message: str):
        """Lida com mensagens de configuração."""
        try:
            # Extrai o número de serviços da mensagem
            num_services = int(message.split(';')[1])
            self.num_services = num_services
            
            # Reconecta com os novos alvos
            time.sleep(2)  # Espera antes de reconectar
            self._create_connection_with_destiny()
            time.sleep(2)  # Espera antes de reconectar
            
            # Envia confirmação
            if self.connection_origin_socket:
                try:
                    self.connection_origin_socket.send(b"Configuration has finished\n")
                except:
                    print("Erro ao enviar confirmação de configuração")
            
        except Exception as e:
            print(f"Erro ao lidar com mensagem de configuração: {e}")

    def _handle_message(self, message: str):
        """Lida com mensagens normais."""
        if len(self.queue) >= self.config['queue_size']:
            print(f"Fila cheia, mensagem descartada: {message}")
            return

        if self.is_destiny_free(self.connection_destiny_sockets[self.current_target_index]):
            try:
                self.connection_destiny_sockets[self.current_target_index].send(message.encode())
                self.current_target_index = (self.current_target_index + 1) % len(self.connection_destiny_sockets)
            except:
                print(f"Erro ao enviar mensagem para destino: {message}")
        else:
            self.queue.append(message)
            print(f"Mensagem adicionada à fila: {message}")

    def _handle_ping_message(self, socket_connection: socket.socket):
        """Lida com mensagens de ping."""
        try:
            socket_connection.send(b"free")
        except Exception as e:
            print(f"Erro ao enviar resposta de ping: {e}")

    def _create_connection_with_destiny(self):
        """Cria conexões com todos os serviços de destino."""
        try:
            # Limpa conexões existentes
            for socket in self.connection_destiny_sockets:
                try:
                    socket.close()
                except:
                    pass
            self.connection_destiny_sockets.clear()
            
            # Cria novas conexões para cada serviço
            for target in self.targets:
                socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_connection.connect((target.host, target.port))
                self.connection_destiny_sockets.append(socket_connection)
            
        except Exception as e:
            print(f"Erro ao criar conexões com destino: {e}")

    def _register_time_when_arrives(self, received_message: str) -> str:
        """Registra o tempo quando a mensagem chega."""
        try:
            string_splited = received_message.split(';')
            last_registered_time_stamp_string = string_splited[-1].strip()
            if not last_registered_time_stamp_string:
                return received_message
                
            time_now = int(time.time() * 1000)
            return f"{received_message}{time_now};{time_now - int(last_registered_time_stamp_string)};"
        except:
            return received_message

    def _register_time_when_goes_out(self, received_message: str) -> str:
        """Registra o tempo quando a mensagem sai."""
        try:
            time_now = int(time.time() * 1000)
            received_message += f"{time_now};"
            string_splited = received_message.split(';')
            if len(string_splited) >= 2:
                last = int(string_splited[-1])
                second_last = int(string_splited[-2])
                return f"{received_message}{last - second_last};"
            return received_message
        except:
            return received_message

    @staticmethod
    def get_random_number() -> int:
        """Gera um número aleatório entre 1000 e 9000."""
        return random.randint(1000, 9000)

    def _process_queue(self):
        """Processa mensagens na fila."""
        while self.is_running and self.queue:
            message = self.queue[0]
            if self.is_destiny_free(self.connection_destiny_sockets[self.current_target_index]):
                try:
                    self.connection_destiny_sockets[self.current_target_index].send(message.encode())
                    self.queue.popleft()
                    self.current_target_index = (self.current_target_index + 1) % len(self.connection_destiny_sockets)
                except:
                    print(f"Erro ao processar mensagem da fila: {message}")
            else:
                break

    def start(self):
        """Inicia o balanceador de carga."""
        super().start()
        # Inicia thread para processar a fila
        import threading
        queue_thread = threading.Thread(target=self._process_queue)
        queue_thread.daemon = True
        queue_thread.start() 