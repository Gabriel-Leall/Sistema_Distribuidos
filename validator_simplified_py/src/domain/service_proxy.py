import socket
import time
from .abstract_proxy import AbstractProxy
from .target_address import TargetAddress

class ServiceProxy(AbstractProxy):
    def __init__(self, target_address: TargetAddress):
        super().__init__()
        self.target_address = target_address
        self.proxy_name = "ServiceProxy"
        self.local_port = 8080

    def _handle_origin_connection(self):
        """Lida com a conexão de origem."""
        try:
            while self.is_running:
                data = self.connection_origin_socket.recv(1024).decode()
                if not data:
                    break
                
                if data.strip() == "ping":
                    self._handle_ping_message(self.connection_origin_socket)
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

    def _handle_ping_message(self, socket_connection: socket.socket):
        """Lida com mensagens de ping."""
        try:
            socket_connection.send(b"free")
        except Exception as e:
            print(f"Erro ao enviar resposta de ping: {e}")

    def _handle_message(self, message: str):
        """Lida com mensagens normais."""
        if self.is_destiny_free(self.connection_destiny_socket):
            try:
                self.connection_destiny_socket.send(message.encode())
            except:
                print(f"Erro ao enviar mensagem para destino: {message}")
        else:
            print(f"Mensagem descartada: {message}")

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