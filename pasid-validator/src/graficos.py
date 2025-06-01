import json
import matplotlib.pyplot as plt
from collections import defaultdict

def gerar_grafico_mrt_por_taxa_geracao(caminho_json: str, modo='num_services', titulo='MRT por Taxa de Geração', nome_arquivo='grafico_mrt.png'):
    """
    Gera gráfico de linha com MRT médio em função da taxa de geração e exporta como PNG.

    modo: 
        - 'num_services': cada linha representa uma quantidade diferente de serviços.
        - 'tipo_servico': cada linha representa um tipo de serviço.
    nome_arquivo:
        - Nome do arquivo PNG a ser salvo.
    """

    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    series = defaultdict(lambda: {'x': [], 'y': []})

    for ciclo in dados.get('cycles', []):
        num_services = ciclo.get('num_services', 0)
        mrt = ciclo.get('mrt_media_ms', 0)
        taxa_geracao = ciclo.get('taxa_geracao', None)

        if taxa_geracao is None:
            continue

        if modo == 'num_services':
            chave = f"{num_services} serviços"
        elif modo == 'tipo_servico':
            chave = ciclo.get('tipo_servico', 'desconhecido')
        else:
            raise ValueError("Modo inválido. Use 'num_services' ou 'tipo_servico'.")

        series[chave]['x'].append(taxa_geracao)
        series[chave]['y'].append(mrt)

    plt.figure(figsize=(10, 6))
    for chave, valores in series.items():
        x = valores['x']
        y = valores['y']
        pares_ordenados = sorted(zip(x, y), key=lambda p: p[0])
        x_ord, y_ord = zip(*pares_ordenados)
        plt.plot(x_ord, y_ord, marker='o', label=chave)

    plt.title(titulo)
    plt.xlabel('Taxa de Geração (msg/s)')
    plt.ylabel('MRT Médio (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300)  # Salva como PNG com alta resolução
    plt.close()  # Fecha a figura para liberar memória
