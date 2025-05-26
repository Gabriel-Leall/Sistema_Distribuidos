import time
from typing import Dict, List
from .source import Source
from .service_proxy import ServiceProxy
from .load_balancer_proxy import LoadBalancerProxy
from .target_address import TargetAddress
from config import BALANCER1, BALANCER2
import json

class LocalTest_Services:
    def __init__(self):
        # Configuração dos serviços
        service_target = TargetAddress("localhost", 8080)
        
        # Cria os balanceadores com as configurações
        self.balancer1 = LoadBalancerProxy(BALANCER1)
        self.balancer2 = LoadBalancerProxy(BALANCER2)
        
        # Cria o service proxy
        self.service_proxy = ServiceProxy(service_target)
        
        # Cria o source
        self.source = Source(self.service_proxy, self.balancer1)
        
        # Configuração dos tempos de transição
        self.transition_times: Dict[str, List[float]] = {
            'T1': [],  # 226.33ms
            'T2': [],  # 72.00ms
            'T3': [],  # 177.00ms
            'T4': [],  # 13.33ms
            'T5': []   # 2030.33ms
        }
        
        # Configuração dos tempos de processamento
        self.processing_times = {
            'T1': 226.33,  # Transição inicial
            'T2': 72.00,   # Transição rápida
            'T3': 177.00,  # Transição média
            'T4': 13.33,   # Transição curta
            'T5': 2030.33  # Transição longa
        }

    def run_test(self, num_iterations: int = 1):
        """
        Executa os testes de transição para cada tipo de serviço.
        
        Args:
            num_iterations (int): Número de iterações para cada transição
        """
        # Inicia os serviços
        print("Iniciando servicos...")
        self.balancer1.start()
        self.balancer2.start()
        self.source.start()
        time.sleep(2)  # Aguarda os serviços iniciarem
        
        # Configura o Source para modo de alimentação do modelo
        self.source.model_feeding_stage = True
        
        print("\nIniciando coleta experimental...")
        print("=" * 50)
        
        # Coleta dos tempos de transição
        for i in range(num_iterations):
            print(f"\nIteracao {i + 1}/{num_iterations}")
            print("-" * 30)
            
            # T1: Transição inicial
            start_time = time.time()
            msg = f"1;0;{int(start_time * 1000)};\n"
            self.source.process_request({"type": "initial", "message": msg})
            time.sleep(self.processing_times['T1'] / 1000)
            end_time = time.time()
            time_diff = (end_time - start_time) * 1000
            self.transition_times['T1'].append(time_diff)
            
            # T2: Transição rápida
            start_time = time.time()
            msg = f"1;1;{int(start_time * 1000)};\n"
            self.source.process_request({"type": "fast", "message": msg})
            time.sleep(self.processing_times['T2'] / 1000)
            end_time = time.time()
            time_diff = (end_time - start_time) * 1000
            self.transition_times['T2'].append(time_diff)
            
            # T3: Transição média
            start_time = time.time()
            msg = f"1;2;{int(start_time * 1000)};\n"
            self.source.process_request({"type": "medium", "message": msg})
            time.sleep(self.processing_times['T3'] / 1000)
            end_time = time.time()
            time_diff = (end_time - start_time) * 1000
            self.transition_times['T3'].append(time_diff)
            
            # T4: Transição curta
            start_time = time.time()
            msg = f"1;3;{int(start_time * 1000)};\n"
            self.source.process_request({"type": "short", "message": msg})
            time.sleep(self.processing_times['T4'] / 1000)
            end_time = time.time()
            time_diff = (end_time - start_time) * 1000
            self.transition_times['T4'].append(time_diff)
            
            # T5: Transição longa
            start_time = time.time()
            msg = f"1;4;{int(start_time * 1000)};\n"
            self.source.process_request({"type": "long", "message": msg})
            time.sleep(self.processing_times['T5'] / 1000)
            end_time = time.time()
            time_diff = (end_time - start_time) * 1000
            self.transition_times['T5'].append(time_diff)

    def print_results(self):
        """Imprime os resultados dos testes."""
        print("\nThe times to feed the models transitions are the following:")
        for transition, times in self.transition_times.items():
            average = sum(times) / len(times)
            print(f"{transition} = {average}")

    def save_results(self, filename: str = "test_results.json"):
        """
        Salva os resultados em um arquivo JSON.
        
        Args:
            filename: Nome do arquivo para salvar os resultados
        """
        results = {
            'transition_times': {
                transition: {
                    'times': times,
                    'average': sum(times) / len(times)
                }
                for transition, times in self.transition_times.items()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4) 