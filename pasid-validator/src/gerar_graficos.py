import re
import matplotlib.pyplot as plt
import os
import sys

# Configuração do estilo dos gráficos
plt.style.use('default')  # Usando estilo padrão do matplotlib
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['axes.facecolor'] = '#f8f9fa'  # Cor de fundo suave
plt.rcParams['grid.color'] = '#dee2e6'      # Cor da grade mais suave
plt.rcParams['axes.edgecolor'] = '#495057'   # Cor das bordas dos eixos

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "graphs")

# Cria a pasta se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def parse_log_file(log_file_path):
    if not os.path.exists(log_file_path):
        print(f"Erro: Arquivo de log não encontrado em {log_file_path}")
        return []

    results = []
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Captura "Iniciando Ciclo N." seguido de "MRT médio: X ms"
        pattern = re.compile(
            r"Iniciando Ciclo (\d+)\..*?MRT médio: ([\d.]+)\s*ms",
            re.DOTALL
        )

        matches = pattern.findall(content)

        for match in matches:
            cycle_number = int(match[0])
            avg_mrt = float(match[1])
            results.append((cycle_number, avg_mrt))

    except Exception as e:
        print(f"Erro ao analisar o arquivo de log: {e}")
    
    return results

def plot_mrt_vs_num_services(data, log_file_name="log.txt"):
    if not data:
        print("Sem dados para plotar.")
        return

    # Ordena os dados pelo número de serviços para um gráfico mais limpo
    data.sort(key=lambda x: x[0])

    num_services = [item[0] for item in data]
    avg_mrts = [item[1] for item in data]

    plt.figure(figsize=(12, 8))
    plt.plot(num_services, avg_mrts, marker='o', linestyle='-', linewidth=2, markersize=8, color='#1f77b4')
    
    plt.title('Tempo Médio de Resposta (MRT) vs. Número de Serviços', pad=20)
    plt.xlabel("Número de Serviços no Ciclo")
    plt.ylabel("Tempo Médio de Resposta (MRT) (ms)")
    plt.xticks(num_services)
    
    # Adiciona grade com estilo mais suave
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Ajusta margens e layout
    plt.tight_layout()
    
    # Salva o gráfico em um arquivo
    plot_filename = os.path.join(output_dir, f"2_mrt_vs_num_servicos_{log_file_name.replace('.txt', '').replace('.', '_')}.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Gráfico salvo como {plot_filename}")

def plot_mrt_vs_generation_rate(experimental_data):
    if not experimental_data:
        print("Sem dados experimentais para plotar.")
        return

    plt.figure(figsize=(12, 8))
    
    # Determina todos os números únicos de serviços em todos os experimentos para plotagem consistente
    all_num_services = sorted(list(set(
        item[0] for delay_data in experimental_data.values() for item in delay_data
    )))

    # Cores para diferentes números de serviços
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    for idx, num_s in enumerate(all_num_services):
        rates = []
        mrts_for_num_s = []
        
        sorted_arrival_delays = sorted(experimental_data.keys())

        for arrival_delay in sorted_arrival_delays:
            data_for_delay = experimental_data[arrival_delay]
            for services, mrt in data_for_delay:
                if services == num_s:
                    generation_rate = 1000.0 / arrival_delay if arrival_delay > 0 else float('inf')
                    rates.append(generation_rate)
                    mrts_for_num_s.append(mrt)
        
        if rates:
            sorted_points = sorted(zip(rates, mrts_for_num_s))
            rates_sorted = [p[0] for p in sorted_points]
            mrts_sorted = [p[1] for p in sorted_points]
            plt.plot(rates_sorted, mrts_sorted, 
                    marker='o', 
                    linestyle='-', 
                    linewidth=2,
                    markersize=8,
                    color=colors[idx % len(colors)],
                    label=f'{num_s + 1} Serviço(s)')

    plt.title('Tempo Médio de Resposta (MRT) vs. Taxa de Geração de Mensagens', pad=20)
    plt.xlabel("Taxa de Geração de Mensagens (mensagens/segundo)")
    plt.ylabel("Tempo Médio de Resposta (MRT) (ms)")
    
    if any(all_num_services):
        plt.legend(title="Número de Serviços", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    plot_filename = os.path.join(output_dir, "2_mrt_vs_taxa_geracao.png")
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Gráfico salvo como {plot_filename}")

if __name__ == "__main__":
    # Lê o arquivo de log
    log_file_to_parse = os.path.abspath(os.path.join(script_dir, '../log.txt'))
    parsed_data_single_log = parse_log_file(log_file_to_parse)

    if not parsed_data_single_log:
        print(f"Não foi possível analisar os dados de {log_file_to_parse} para o primeiro gráfico.")
        sys.exit(1)

    print("\n---\n")

    # Gera o primeiro gráfico
    plot_mrt_vs_num_services(parsed_data_single_log, os.path.basename(log_file_to_parse))

    # Prepara dados para o segundo gráfico
    simulated_experimental_data = {}
    
    # Arrival delays em milissegundos (quanto menor, maior a taxa de chegada)
    arrival_delays = [7500, 5000, 2000, 1000, 500, 250]  # crescente taxa de chegada
    real_arrival_delay = 2000  # <--- altere este valor para o usado no seu experimento real

    for delay in arrival_delays:
        # Fator proporcional ao inverso da taxa (taxa = 1/delay)
        fator = real_arrival_delay / delay
        simulated_experimental_data[delay] = [(s, mrt * fator) for s, mrt in parsed_data_single_log]

    if simulated_experimental_data:
        print("Dados experimentais simulados para plotar MRT vs. Taxa de Geração:")
        for delay, data in sorted(simulated_experimental_data.items()):
            print(f"  Atraso de Chegada: {delay}ms, Dados: {data}")
        plot_mrt_vs_generation_rate(simulated_experimental_data)
    else:
        print("Não há dados suficientes para demonstrar o gráfico MRT vs. Taxa de Geração.")

    if plt.get_fignums(): # Verifica se alguma figura foi criada
        plt.show() 