import socket
import threading
from typing import Optional
from .target_address import TargetAddress

class AbstractProxy:
    def __init__(self):
        self.proxy_name = ""
        self.local_port = 0
        self.target_address: Optional[TargetAddress] = None
        self.connection_origin_socket: Optional[socket.socket] = None
        self.connection_destiny_socket: Optional[socket.socket] = None
        self.origin_thread: Optional[threading.Thread] = None
        self.destiny_thread: Optional[threading.Thread] = None
        self.is_running = True

    def start(self):
        """Inicia o proxy."""
        self.origin_thread = threading.Thread(target=self._connection_establishment_origin_thread)
        self.destiny_thread = threading.Thread(target=self._connection_establishment_destiny_thread)
        
        self.origin_thread.start()
        self.destiny_thread.start()

    def stop(self):
        """Para o proxy."""
        self.is_running = False
        if self.connection_origin_socket:
            self.connection_origin_socket.close()
        if self.connection_destiny_socket:
            self.connection_destiny_socket.close()

    def _connection_establishment_origin_thread(self):
        """Thread para estabelecer conexão com a origem."""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('localhost', self.local_port))
            server_socket.listen(1)
            
            while self.is_running:
                self.connection_origin_socket, _ = server_socket.accept()
                self._handle_origin_connection()
                
        except Exception as e:
            print(f"Erro na thread de origem: {e}")
        finally:
            server_socket.close()

    def _connection_establishment_destiny_thread(self):
        """Thread para estabelecer conexão com o destino."""
        try:
            while self.is_running:
                if self.target_address:
                    self.connection_destiny_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.connection_destiny_socket.connect((self.target_address.host, self.target_address.port))
                    self._handle_destiny_connection()
                    
        except Exception as e:
            print(f"Erro na thread de destino: {e}")

    def _handle_origin_connection(self):
        """Método para lidar com a conexão de origem."""
        raise NotImplementedError("Subclasses devem implementar este método")

    def _handle_destiny_connection(self):
        """Método para lidar com a conexão de destino."""
        raise NotImplementedError("Subclasses devem implementar este método")

    def is_destiny_free(self, socket_connection: Optional[socket.socket]) -> bool:
        """Verifica se o destino está livre."""
        if not socket_connection:
            return False
        try:
            socket_connection.send(b"ping")
            response = socket_connection.recv(1024).decode()
            return response == "free"
        except:
            return False 