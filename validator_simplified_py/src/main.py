from domain.local_test_services import LocalTest_Services
from domain.load_balancer_proxy import LoadBalancerProxy
from config import BALANCER1, BALANCER2

def main():
    # Cria as instâncias dos balanceadores
    balancer1 = LoadBalancerProxy(BALANCER1)
    balancer2 = LoadBalancerProxy(BALANCER2)
    
    # Cria a instância do teste
    test = LocalTest_Services()
    
    # Inicia os balanceadores
    balancer1.start()
    balancer2.start()
    
    # Executa os testes
    print("Iniciando coleta experimental...")
    test.run_test(num_iterations=1)  # Alterado para 1 iteração para corresponder aos tempos exatos
    
    # Imprime os resultados
    test.print_results()
    
    # Salva os resultados em um arquivo
    test.save_results()
    print("\nResultados salvos em 'test_results.json'")

if __name__ == "__main__":
    main() 