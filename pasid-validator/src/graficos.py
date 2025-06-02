import json
import matplotlib.pyplot as plt
import numpy as np

def gerar_graficos_mrt(nome_arquivo: str = "resultados/resultados_mrt.json"):
    """Gera 3 tipos de gráficos de linha analisando o MRT a partir do arquivo JSON"""
    
    # Carrega os dados do arquivo
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    if not dados['cycles']:
        print("Nenhum dado de ciclo encontrado para gerar gráficos")
        return
    
    # Gráfico 1: Evolução do MRT médio por ciclo
    plt.figure(figsize=(10, 6))
    for ciclo in dados['cycles']:
        if 'alimentacao' in ciclo:
            continue  # Pula ciclos de alimentação
            
        # Calcula MRT médio para cada mensagem no ciclo (suavizado)
        tempos = ciclo['tempos_ms']
        mrt_cumulativo = [np.mean(tempos[:i+1]) for i in range(len(tempos))]
        
        plt.plot(range(1, len(tempos)+1), mrt_cumulativo, 
                label=f"{ciclo['num_services']} serviço(s)")
    
    plt.title("Evolução do MRT Médio por Mensagem (Cumulativo)")
    plt.xlabel("Número da Mensagem")
    plt.ylabel("MRT (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig("resultados/mrt_evolucao_cumulativa.png")
    plt.close()
    
    # Gráfico 2: Comparação de MRT por quantidade de serviços
    plt.figure(figsize=(10, 6))
    servicos_mrt = {}
    
    for ciclo in dados['cycles']:
        if 'alimentacao' in ciclo:
            continue
            
        num_serv = ciclo['num_services']
        if num_serv not in servicos_mrt:
            servicos_mrt[num_serv] = []
        servicos_mrt[num_serv].extend(ciclo['tempos_ms'])
    
    for num_serv, tempos in servicos_mrt.items():
        # Agrupa tempos em lotes para suavizar
        lotes = [tempos[i:i+10] for i in range(0, len(tempos), 10)]
        medias = [np.mean(lote) for lote in lotes if lote]
        
        plt.plot(range(len(medias)), medias, 
               label=f"{num_serv} serviço(s)", 
               marker='o')
    
    plt.title("MRT por Quantidade de Serviços")
    plt.xlabel("Lote de Mensagens (10 mensagens/lote)")
    plt.ylabel("MRT (ms)")
    plt.legend()
    plt.grid(True)
    plt.savefig("resultados/mrt_por_servico.png")
    plt.close()
    
    # Gráfico 3: Distribuição dos MRTs individuais
    plt.figure(figsize=(12, 6))
    
    for ciclo in dados['cycles']:
        if 'alimentacao' in ciclo:
            continue
            
        tempos = ciclo['tempos_ms']
        plt.plot(tempos, 
               label=f"Ciclo {ciclo['cycle_index']} - {ciclo['num_services']} serviço(s)",
               alpha=0.6)
    
    plt.title("Distribuição Individual dos Tempos de Resposta")
    plt.xlabel("Número da Mensagem")
    plt.ylabel("MRT Individual (ms)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/mrt_distribuicao_individual.png")
    plt.close()

    print("Gráficos gerados em: resultados/mrt_*.png")