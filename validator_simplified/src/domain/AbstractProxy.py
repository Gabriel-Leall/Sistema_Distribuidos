import socket
import threading
import time

class AbstractProxy(threading.Thread):

    def __init__(self, proxy_name: str, local_port: int):
        super().__init__()
        self.proxy_name = proxy_name
        self.local_port = local_port
        self.content_to_process = None
        self.local_socket = None
        self.connection_destiny_socket = None

    class ReceiverThread(threading.Thread):

        def __init__(self, new_socket_connection: socket.socket, parent):
            super().__init__()
            self.new_socket_connection = new_socket_connection
            self.parent = parent

        def run(self):
            try:
                self.parent.receiving_messages(self.new_socket_connection)
            except (IOError, InterruptedError) as e:
                raise RuntimeError(e)

    class ConnectionEstablishmentOriginThread(threading.Thread):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent

        def run(self):
            try:
                self.parent.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.parent.local_socket.bind(("", self.parent.local_port))
                self.parent.local_socket.listen()
                while True:
                    new_connection, _ = self.parent.local_socket.accept()
                    self.parent.ReceiverThread(new_connection, self.parent).start()
            except IOError as e:
                raise RuntimeError(e)

    class ConnectionEstablishmentDestinyThread(threading.Thread):

        def __init__(self, parent):
            super().__init__()
            self.parent = parent

        def run(self):
            connected = False
            while not connected:
                try:
                    time.sleep(0.001)
                    self.parent.create_connection_with_destiny()
                    connected = True
                except (IOError, InterruptedError):
                    pass

    def has_something_to_process(self) -> bool:
        return self.content_to_process is not None

    def set_content_to_process(self, content_to_process: str):
        self.content_to_process = content_to_process

    def is_destiny_free(self, connection_socket: socket.socket) -> bool:
        try:
            connection_socket.sendall(b"ping\n")
            message = connection_socket.recv(1024).decode()
            return message == "free"
        except (IOError, ValueError):
            return False

    def send_message_to_destiny(self, file_content: str, connection_socket: socket.socket = None):
        if connection_socket is None:
            connection_socket = self.connection_destiny_socket
        connection_socket.sendall(file_content.encode())

    def create_connection_with_destiny(self):
        raise NotImplementedError("Subclasses must implement this method")

    def receiving_messages(self, connection_socket: socket.socket):
        raise NotImplementedError("Subclasses must implement this method")
