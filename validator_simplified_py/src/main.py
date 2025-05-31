from domain.local_test_services import LocalTest_Services
import time

def main():
    print("\n=== Iniciando Teste de Balanceamento de Carga ===")
    
    # Cria a instância do teste
    test = LocalTest_Services()
    
    # Aguarda um momento para garantir que tudo foi inicializado
    print("\nAguardando inicialização dos serviços...")
    time.sleep(2)
    
    try:
        # Executa os testes
        print("\n=== Iniciando Execução dos Testes ===")
        test.run_test(num_iterations=10)
        
        # Imprime os resultados
        print("\n=== Resultados dos Testes ===")
        test.print_results()
        
        # Salva os resultados em um arquivo
        test.save_results()
        
    except Exception as e:
        print(f"\nErro durante a execução dos testes: {str(e)}")
    finally:
        print("\n=== Finalizando Teste ========")

if __name__ == "__main__":
    main() 