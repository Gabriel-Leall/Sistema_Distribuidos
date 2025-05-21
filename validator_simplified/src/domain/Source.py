import socket
import threading
import time
import random
import json
from typing import List
from AbstractProxy import AbstractProxy
from TargetAddress import TargetAddress

class Source(AbstractProxy):

    def __init__(self, name: str, local_port: int, max_considered_messages_expected: int,
                 target_address: TargetAddress, arrival_delay: int, model_feeding_stage: bool,
                 variated_server_load_balancer_ip: str, variated_server_load_balancer_port: int,
                 qtd_services: List[int], mrts_from_model: List[float], sdvs_from_model: List[float]):
        super().__init__(name, local_port)
        self.model_feeding_stage = model_feeding_stage
        self.target_address = target_address
        self.arrival_delay = arrival_delay
        self.max_considered_messages_expected = max_considered_messages_expected
        self.variated_server_load_balancer_ip = variated_server_load_balancer_ip
        self.variated_server_load_balancer_port = variated_server_load_balancer_port
        self.qtd_services = qtd_services
        self.mrts_from_model = mrts_from_model
        self.sdvs_from_model = sdvs_from_model
        self.considered_messages = []
        self.cycles_completed = [False] * len(qtd_services)
        self.dropp_count = 0
        self.all_cycles_completed = False
        self.experiment_data = []
        self.experiment_error = []

    def run(self):
        threading.Thread(target=self.ConnectionEstablishmentOriginThread(self).run).start()
        threading.Thread(target=self.ConnectionEstablishmentDestinyThread(self).run).start()
        time.sleep(0.1)
        print("Starting source")

        if self.model_feeding_stage:
            self.send_message_feeding_stage()
        else:
            self.send_messages_validation_stage()

    def send_message_feeding_stage(self):
        self.arrival_delay = 2000
        print("ATTENTION: Guarantee that arrival delay is a higher value than the sum of all service times.")
        print("##############################")
        print("Model Feeding Stage Started")
        print("##############################")
        print(f"Only 10 requests will be generated with AD = {self.arrival_delay}ms")
        time.sleep(5)

        for j in range(10):
            msg = f"1;{j};{int(time.time() * 1000)};\n"
            self.send(msg)
            time.sleep(self.arrival_delay / 1000)

    def send_messages_validation_stage(self):
        for cycle, qts in enumerate(self.qtd_services):
            self.considered_messages.clear()
            config_message = f"config;{qts};\n"
            self.send_message_to_configure_server(config_message)
            time.sleep(5)

            for j in range(self.max_considered_messages_expected):
                msg = f"{cycle};{j};{int(time.time() * 1000)};\n"
                self.send(msg)

            while not self.cycles_completed[cycle]:
                time.sleep(1)

    def send_message_to_configure_server(self, config_message: str):
        for attempt in range(5):
            try:
                with socket.create_connection((self.variated_server_load_balancer_ip, self.variated_server_load_balancer_port)) as sock:
                    sock.sendall(config_message.encode())
                    response = sock.recv(1024).decode()
                    print(f"Received response from variatedServer: {response}")
                    return
            except (socket.error, IOError):
                print("Error sending configuration message to variatedServer, retrying...")
                time.sleep(2)
        raise RuntimeError("Failed to connect to variatedServer after 5 attempts")

    def send(self, msg: str):
        if self.is_destiny_free(self.connection_destiny_socket):
            self.send_message_to_destiny(msg)
        else:
            print(f"DROPPED IN SOURCE {msg}")
            self.dropp_count += 1
        time.sleep(self.arrival_delay / 1000)

    def receiving_messages(self, new_socket_connection: socket.socket):
        print(f"{self.proxy_name} enabled to receive messages.")
        with new_socket_connection.makefile('r') as reader:
            for received_message in reader:
                received_message = self.register_mrt_at_the_end(received_message.strip())
                if self.model_feeding_stage:
                    self.execute_first_stage_of_model_feeding(received_message)
                else:
                    self.execute_second_stage_of_validation(received_message)

    def register_mrt_at_the_end(self, received_message: str) -> str:
        parts = received_message.split(';')
        last = int(parts[-2])
        first = int(parts[2])
        current_mrt = last - first
        return f"{received_message}RESPONSE TIME:;{current_mrt};"

    def execute_first_stage_of_model_feeding(self, received_message: str):
        self.considered_messages.append(received_message)
        print(received_message)

    def execute_second_stage_of_validation(self, received_message: str):
        self.considered_messages.append(received_message)
        print(received_message)
