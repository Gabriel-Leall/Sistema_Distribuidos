import socket
import random
import time
import threading
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
        
        # Criar socket de origem
        self.connection_origin_socket = None
        self.server_socket = None
        
        print(f"Balanceador {self.proxy_name} inicializado na porta {self.local_port}")

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
            print(f"Serviço {i+1} criado na porta {service.port}")
        return services

    def _handle_origin_connection(self):
        """Lida com a conexão de origem."""
        try:
            print(f"Balanceador {self.proxy_name} aguardando mensagens...")
            while self.is_running:
                data = self.connection_origin_socket.recv(1024).decode()
                if not data:
                    break
                
                print(f"Balanceador {self.proxy_name} recebeu mensagem: {data.strip()}")
                
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
            print(f"Balanceador {self.proxy_name} aguardando respostas dos serviços...")
            while self.is_running:
                for socket in self.connection_destiny_sockets:
                    try:
                        data = socket.recv(1024).decode()
                        if not data:
                            continue
                        
                        print(f"Balanceador {self.proxy_name} recebeu resposta: {data.strip()}")
                        
                        # Verifica se é uma mensagem de ping
                        if data.strip() == "ping":
                            self._handle_ping_message(socket)
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
                                print(f"Balanceador {self.proxy_name} enviou resposta para origem")
                            except:
                                print("Erro ao enviar resposta para origem")
                    except:
                        continue
                
        except Exception as e:
            print(f"Erro ao lidar com conexão de destino: {e}")
        finally:
            for socket in self.connection_destiny_sockets:
                try:
                    socket.close()
                except:
                    pass

    def _handle_config_message(self, message: str):
        """Lida com mensagens de configuração."""
        try:
            print(f"Balanceador {self.proxy_name} recebeu mensagem de configuração")
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
                    print(f"Balanceador {self.proxy_name} enviou confirmação de configuração")
                except:
                    print("Erro ao enviar confirmação de configuração")
            
        except Exception as e:
            print(f"Erro ao lidar com mensagem de configuração: {e}")

    def _handle_message(self, message: str):
        """Lida com mensagens normais."""
        print(f"Balanceador {self.proxy_name} processando mensagem: {message.strip()}")
        
        if len(self.queue) >= self.config['queue_size']:
            print(f"Fila cheia, mensagem descartada: {message}")
            return

        if self.is_destiny_free(self.connection_destiny_sockets[self.current_target_index]):
            try:
                self.connection_destiny_sockets[self.current_target_index].send(message.encode())
                print(f"Balanceador {self.proxy_name} enviou mensagem para serviço {self.current_target_index + 1}")
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
            print(f"Balanceador {self.proxy_name} respondeu ping")
        except Exception as e:
            print(f"Erro ao enviar resposta de ping: {e}")

    def _create_connection_with_destiny(self):
        """Cria conexões com todos os serviços de destino."""
        try:
            print(f"Balanceador {self.proxy_name} criando conexões com serviços...")
            # Limpa conexões existentes
            for socket in self.connection_destiny_sockets:
                try:
                    socket.close()
                except:
                    pass
            self.connection_destiny_sockets.clear()
            
            # Cria novas conexões para cada serviço
            for i, target in enumerate(self.targets):
                socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_connection.connect((target.host, target.port))
                self.connection_destiny_sockets.append(socket_connection)
                print(f"Balanceador {self.proxy_name} conectado ao serviço {i+1} na porta {target.port}")
            
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
        print(f"Balanceador {self.proxy_name} iniciando processamento da fila...")
        while self.is_running and self.queue:
            message = self.queue[0]
            if self.is_destiny_free(self.connection_destiny_sockets[self.current_target_index]):
                try:
                    self.connection_destiny_sockets[self.current_target_index].send(message.encode())
                    print(f"Balanceador {self.proxy_name} processou mensagem da fila para serviço {self.current_target_index + 1}")
                    self.queue.popleft()
                    self.current_target_index = (self.current_target_index + 1) % len(self.connection_destiny_sockets)
                except:
                    print(f"Erro ao processar mensagem da fila: {message}")
            else:
                break

    def start(self):
        """Inicia o balanceador de carga."""
        try:
            print(f"Iniciando balanceador {self.proxy_name}...")
            # Cria o socket do servidor
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('localhost', self.local_port))
            self.server_socket.listen(1)
            
            print(f"Balanceador {self.proxy_name} aguardando conexão de origem...")
            # Aceita conexão de origem
            self.connection_origin_socket, _ = self.server_socket.accept()
            print(f"Balanceador {self.proxy_name} aceitou conexão de origem")
            
            # Cria conexões com os serviços
            self._create_connection_with_destiny()
            
            # Inicia thread para processar a fila
            queue_thread = threading.Thread(target=self._process_queue)
            queue_thread.daemon = True
            queue_thread.start()
            
            # Inicia thread para lidar com conexão de origem
            origin_thread = threading.Thread(target=self._handle_origin_connection)
            origin_thread.daemon = True
            origin_thread.start()
            
            # Inicia thread para lidar com conexão de destino
            destiny_thread = threading.Thread(target=self._handle_destiny_connection)
            destiny_thread.daemon = True
            destiny_thread.start()
            
            self.is_running = True
            print(f"Balanceador {self.proxy_name} iniciado com sucesso")
            
        except Exception as e:
            print(f"Erro ao iniciar balanceador: {e}")
            self.stop()

    def stop(self):
        """Para o balanceador de carga."""
        print(f"Parando balanceador {self.proxy_name}...")
        self.is_running = False
        
        # Fecha conexões
        if self.connection_origin_socket:
            try:
                self.connection_origin_socket.close()
            except:
                pass
                
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
                
        for socket in self.connection_destiny_sockets:
            try:
                socket.close()
            except:
                pass
        print(f"Balanceador {self.proxy_name} parado") 