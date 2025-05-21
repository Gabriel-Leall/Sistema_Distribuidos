import socket
import threading
import random
import time
from typing import List
from AbstractProxy import AbstractProxy
from TargetAddress import TargetAddress
from ServiceProxy import ServiceProxy
from domain.utils import Utils

class LoadBalancerProxy(AbstractProxy):

    def __init__(self, config_path: str):
        super().__init__("load_balancer", 0)
        self.service_addresses = []
        self.queue_load_balancer_max_size = 0
        self.queue = []
        self.connection_destiny_sockets = []
        self.qtd_services_list = []
        self.index_current_qtd_services = 0
        self.service_time = 0.0
        self.service_time_standard_deviation = 0.0
        self.target_is_source = False
        self.service_target_ip = ""
        self.service_target_port = 0
        self.services = []
        self.sent_config_messages = set()

        self.load_config(config_path)
        self.service_addresses = self.create_services(
            self.local_port,
            self.service_target_port,
            self.service_time,
            self.service_target_ip,
            self.target_is_source,
            self.service_time_standard_deviation
        )
        self.target_address = self.service_addresses[0]
        self.print_load_balancer_parameters()

    def load_config(self, config_path: str):
        import configparser
        config = configparser.ConfigParser()
        config.read(config_path)

        self.proxy_name = config.get("server", "loadBalancerName")
        self.local_port = config.getint("server", "loadBalancerPort")
        self.queue_load_balancer_max_size = config.getint("server", "queueLoadBalancerMaxSize")
        self.qtd_services_list = [config.getint("server", "qtdServices")]

        self.service_target_ip = config.get("service", "serviceTargetIp")
        self.service_target_port = config.getint("service", "serviceTargetPort")
        self.service_time = config.getfloat("service", "serviceTime")
        self.service_time_standard_deviation = config.getfloat("service", "std")
        self.target_is_source = config.getboolean("service", "targetIsSource")

    def print_load_balancer_parameters(self):
        print("======================================")
        print("Load Balancer Parameters:")
        print(f"Load Balancer Name: {self.proxy_name}")
        print(f"Local Port: {self.local_port}")
        print(f"Queue Load Balancer Max Size: {self.queue_load_balancer_max_size}")
        print(f"Qtd Services List: {self.qtd_services_list}")
        print("======================================")

    def create_services(self, load_balancer_port: int, target_port: int, service_time: float, target_ip: str, target_is_source: bool, std: float) -> List[TargetAddress]:
        service_addresses = []
        port = load_balancer_port + 1
        qtd_services_in_this_cycle = self.qtd_services_list[0]

        while qtd_services_in_this_cycle > 0:
            ta = TargetAddress("localhost", port)
            service_proxy = ServiceProxy(f"service{port}", port, TargetAddress(target_ip, target_port), service_time, std, target_is_source)
            self.services.append(service_proxy)
            service_proxy.start()
            service_addresses.append(ta)

            port += 1
            qtd_services_in_this_cycle -= 1

        return service_addresses

    def create_connection_with_destiny(self):
        for target_address in self.service_addresses:
            self.connection_destiny_sockets.append(socket.create_connection((target_address.ip, target_address.port)))

    def has_something_to_process(self) -> bool:
        return bool(self.queue)

    def run(self):
        threading.Thread(target=self.ConnectionEstablishmentOriginThread(self).run).start()
        threading.Thread(target=self.ConnectionEstablishmentDestinyThread(self).run).start()
        print(f"Starting {self.proxy_name}")

        while True:
            if self.has_something_to_process():
                not_sent_yet = True
                while not_sent_yet:
                    for connection_socket in self.connection_destiny_sockets:
                        if self.is_destiny_free(connection_socket):
                            msg = self.queue.pop(0)
                            self.send_message_to_destiny(msg, connection_socket)
                            not_sent_yet = False
                            break

    def receiving_messages(self, connection_socket: socket.socket):
        print(f"{self.proxy_name} enabled to receive messages.")
        with connection_socket.makefile('r') as reader:
            for received_message in reader:
                received_message = received_message.strip()
                if "config" in received_message:
                    self.change_service_targets_of_this_server(received_message, connection_socket)
                elif received_message == "ping":
                    self.handle_ping_message(connection_socket)
                else:
                    self.handle_message(received_message)

    def handle_ping_message(self, connection_socket: socket.socket):
        with connection_socket.makefile('w') as writer:
            if len(self.queue) < self.queue_load_balancer_max_size:
                writer.write("free\n")
            else:
                writer.write("busy\n")
            writer.flush()

    def handle_message(self, received_message: str):
        received_message = Utils.registerTime(received_message)
        received_message += f"{int(time.time() * 1000)};\n"
        self.queue.append(received_message)

    def change_service_targets_of_this_server(self, received_message: str, connection_socket: socket.socket):
        parts = received_message.split(';')
        # Clear existing services and stop them
        for service_proxy in self.services:
            service_proxy.stop_service()
        self.services.clear()
        self.service_addresses.clear()

        # Update service addresses with new targets
        self.index_current_qtd_services += 1
        qtd_services_in_this_cycle = int(parts[1])

        for _ in range(qtd_services_in_this_cycle):
            service_port = random.randint(1000, 9000)
            service_proxy = ServiceProxy(
                f"service{service_port}",  # Nome do serviço
                service_port,  # Porta do serviço
                TargetAddress(self.service_target_ip, self.service_target_port),  # Endereço de destino
                self.service_time,  # Tempo de serviço, substitua este valor conforme necessário
                self.service_time_standard_deviation,  # Desvio padrão (std), substitua este valor conforme necessário
                self.target_is_source  # targetIsSource, ajuste conforme necessário
            )

            service_proxy.start()
            self.services.append(service_proxy)
            self.service_addresses.append(TargetAddress("localhost", service_port))

        # Update target address to the first one in the new list
        self.target_address = self.service_addresses[0]

        # Introduce a delay before reconnecting (optional)
        time.sleep(2)
        self.create_connection_with_destiny()
        time.sleep(2)
        with connection_socket.makefile('w') as writer:
            writer.write("Configuration has finished\n")
            writer.flush()
