from domain.local_test_services import LocalTest_Services

def main():
    # Cria a instância do teste
    test = LocalTest_Services()
    
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