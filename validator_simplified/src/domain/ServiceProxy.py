import socket
import threading
import time
import random

from AbstractProxy import AbstractProxy
from TargetAddress import TargetAddress

class ServiceProxy(AbstractProxy):

    def __init__(self, name: str, local_port: int, target_address: TargetAddress, service_time: float, std: float, target_is_source: bool):
        super().__init__(name, local_port)
        self.target_is_source = target_is_source
        self.target_address = target_address
        self.service_time = service_time
        self.std = std
        self.interrupt = False
        self.content_to_process = None

    def run(self):
        threading.Thread(target=self.ConnectionEstablishmentOriginThread(self).run).start()
        threading.Thread(target=self.ConnectionEstablishmentDestinyThread(self).run).start()
        print(f"Starting {self.proxy_name}")

        while not self.interrupt:
            self.process_and_send_to_destiny()

    def process_and_send_to_destiny(self):
        if self.has_something_to_process():
            val = random.gauss(self.service_time, self.std)
            self.content_to_process += f"{int(time.time() * 1000)};"
            time.sleep(val / 1000)  # Convert milliseconds to seconds

            if self.target_is_source:
                self.content_to_process = self.register_time_when_go_out(self.content_to_process)

            try:
                if self.target_is_source:
                    self.send_message_to_destiny(self.content_to_process + "\n")
                else:
                    while True:
                        if self.is_destiny_free(self.connection_destiny_socket):
                            self.send_message_to_destiny(self.content_to_process + "\n")
                            break
                        time.sleep(0.1)
            except (IOError, ValueError) as e:
                raise RuntimeError(e)

            self.content_to_process = None

    def stop_service(self):
        self.interrupt = True

    def create_connection_with_destiny(self):
        self.connection_destiny_socket = socket.create_connection((self.target_address.ip, self.target_address.port))

    def receiving_messages(self, connection_socket: socket.socket):
        print(f"{self.proxy_name} enabled to receive messages.")

        with connection_socket.makefile('r') as reader:
            while True:
                received_message = reader.readline().strip()

                if not received_message:
                    continue

                if received_message == "ping":
                    self.handle_ping_message(connection_socket)
                else:
                    received_message = self.register_time_when_arrives(received_message)
                    self.set_content_to_process(received_message)

    def handle_ping_message(self, connection_socket: socket.socket):
        with connection_socket.makefile('w') as writer:
            if self.has_something_to_process():
                writer.write("busy\n")
            else:
                writer.write("free\n")
            writer.flush()

    @staticmethod
    def register_time_when_arrives(received_message: str) -> str:
        string_splited = received_message.split(';')
        last_registered_time_stamp_string = string_splited[-1]
        time_now = int(time.time() * 1000)
        received_message += f"{time_now};{time_now - int(last_registered_time_stamp_string.strip())};"
        return received_message

    def register_time_when_go_out(self, received_message: str) -> str:
        received_message += f"{int(time.time() * 1000)};"
        timestamps = list(map(int, received_message.split(';')[-3:]))
        received_message += f"{timestamps[-1] - timestamps[-2]};"
        return received_message
