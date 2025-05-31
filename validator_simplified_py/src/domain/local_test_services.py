import time
import random
from datetime import datetime
from typing import List, Dict
import json
import statistics

class LocalTest_Services:
    def __init__(self):
        self.results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0,
            'requests_per_service': {},
            'errors': [],
            'cycles': [],
            'current_cycle': {
                'messages': [],
                'mrt': [],
                'start_time': None
            },
            'load_balancer_usage': {
                'balancer1': 0,
                'balancer2': 0
            }
        }
        
        # Configuração dos serviços
        self.services = {
            'service1': {'port': 4001, 'time_ms': 100},
            'service2': {'port': 4002, 'time_ms': 200},
            'service3': {'port': 4003, 'time_ms': 150},
            'service4': {'port': 4004, 'time_ms': 300}
        }
        
        # Configuração dos balanceadores
        self.load_balancers = {
            'balancer1': {'port': 2000, 'services': ['service1', 'service2']},
            'balancer2': {'port': 3000, 'services': ['service3', 'service4']}
        }
        
        # Inicializa contadores para cada serviço
        for service in self.services:
            self.results['requests_per_service'][service] = 0

    def select_load_balancer(self) -> str:
        """Seleciona um balanceador de carga usando round-robin"""
        if self.results['load_balancer_usage']['balancer1'] <= self.results['load_balancer_usage']['balancer2']:
            self.results['load_balancer_usage']['balancer1'] += 1
            return 'balancer1'
        else:
            self.results['load_balancer_usage']['balancer2'] += 1
            return 'balancer2'

    def simulate_request(self, cycle: int, message_id: int) -> bool:
        """Simula uma requisição passando por um balanceador de carga"""
        # Seleciona um balanceador
        balancer = self.select_load_balancer()
        print(f"\nUsando {balancer} (porta {self.load_balancers[balancer]['port']})")
        
        # Seleciona um serviço do balanceador escolhido
        service_name = random.choice(self.load_balancers[balancer]['services'])
        service = self.services[service_name]
        
        # Timestamps para cálculo do MRT
        send_time = time.time()
        receive_time = send_time + (service['time_ms'] / 1000)
        process_time = receive_time + 0.005  # 5ms de processamento
        response_time = process_time + 0.1   # 100ms de resposta
        
        # Calcula o MRT (Mean Response Time)
        mrt = (response_time - send_time) * 1000  # Converte para milissegundos
        
        # Formata a mensagem similar ao Pasid-Validator
        message = f"{cycle};{message_id};{send_time:.6f};{receive_time:.6f};{process_time:.6f};{response_time:.6f}"
        
        # Simula uma taxa de sucesso de 95%
        success = random.random() < 0.95
        
        if success:
            self.results['successful_requests'] += 1
            self.results['requests_per_service'][service_name] += 1
            self.results['current_cycle']['messages'].append(message)
            self.results['current_cycle']['mrt'].append(mrt)
            print(f"[Ciclo {cycle}] Mensagem considerada: '{message}' | Tempo de resposta (MRT): {mrt:.2f} ms")
        else:
            self.results['failed_requests'] += 1
            self.results['errors'].append({
                'service': service_name,
                'balancer': balancer,
                'timestamp': datetime.now().isoformat(),
                'error': 'Simulated error'
            })
        
        self.results['total_requests'] += 1
        return success

    def run_test(self, num_iterations: int = 10):
        """Executa o teste de balanceamento de carga"""
        print("\n=== Iniciando etapa de envio ===")
        for i in range(num_iterations):
            print(f"Enviando: 1;{i};{time.time():.6f}")
            time.sleep(1)  # Simula delay entre mensagens
        
        print("\n=== Iniciando etapa de validação ===")
        print("Loadbalancer addresses: localhost:2000,localhost:3000")
        start_time = time.time()
        
        # Executa 2 ciclos de teste
        for cycle in range(2):
            self.results['current_cycle'] = {
                'messages': [],
                'mrt': [],
                'start_time': time.time()
            }
            
            # Envia 10 mensagens por ciclo
            for msg_id in range(1, 11):
                self.simulate_request(cycle, msg_id)
            
            # Calcula e exibe estatísticas do ciclo
            if self.results['current_cycle']['mrt']:
                avg_mrt = statistics.mean(self.results['current_cycle']['mrt'])
                std_mrt = statistics.stdev(self.results['current_cycle']['mrt']) if len(self.results['current_cycle']['mrt']) > 1 else 0
                
                print(f"\nCiclo {cycle} finalizado.")
                print(f"Mensagens consideradas: {len(self.results['current_cycle']['messages'])}")
                print(f"MRT médio: {avg_mrt:.2f} ms")
                print(f"Desvio padrão do MRT: {std_mrt:.2f} ms")
                print("=" * 30)
            
            self.results['cycles'].append(self.results['current_cycle'])
        
        self.results['total_time'] = time.time() - start_time

    def print_results(self):
        """Imprime os resultados do teste"""
        print("\nResultados do Teste de Balanceamento de Carga:")
        print(f"Total de requisições: {self.results['total_requests']}")
        print(f"Requisições bem-sucedidas: {self.results['successful_requests']}")
        print(f"Requisições com falha: {self.results['failed_requests']}")
        print(f"Tempo total de execução: {self.results['total_time']:.2f} segundos")
        
        print("\nUso dos Balanceadores de Carga:")
        print(f"Balanceador 1 (porta 2000): {self.results['load_balancer_usage']['balancer1']} requisições")
        print(f"Balanceador 2 (porta 3000): {self.results['load_balancer_usage']['balancer2']} requisições")
        
        print("\nRequisições por serviço:")
        for service, count in self.results['requests_per_service'].items():
            print(f"{service}: {count} requisições")
        
        if self.results['errors']:
            print("\nErros encontrados:")
            for error in self.results['errors']:
                print(f"- Serviço {error['service']} (via {error['balancer']}) em {error['timestamp']}: {error['error']}")

    def save_results(self, filename: str = 'test_results.json'):
        """Salva os resultados em um arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\nResultados salvos em {filename}") 