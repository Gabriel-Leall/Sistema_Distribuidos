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
        self.server_socket: Optional[socket.socket] = None

    def start(self):
        """Inicia o proxy."""
        try:
            # Cria o socket do servidor
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('localhost', self.local_port))
            self.server_socket.listen(1)
            
            # Aceita conexão de origem
            self.connection_origin_socket, _ = self.server_socket.accept()
            
            # Inicia thread para lidar com conexão de origem
            self.origin_thread = threading.Thread(target=self._handle_origin_connection)
            self.origin_thread.daemon = True
            self.origin_thread.start()
            
            # Inicia thread para lidar com conexão de destino
            self.destiny_thread = threading.Thread(target=self._handle_destiny_connection)
            self.destiny_thread.daemon = True
            self.destiny_thread.start()
            
        except Exception as e:
            print(f"Erro ao iniciar proxy: {e}")
            self.stop()

    def stop(self):
        """Para o proxy."""
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
                
        if self.connection_destiny_socket:
            try:
                self.connection_destiny_socket.close()
            except:
                pass

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