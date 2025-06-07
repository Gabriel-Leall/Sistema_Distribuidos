import socket
import datetime
import time
from typing import List, Dict, Any, Optional, Tuple
from src.abstract_proxy import AbstractProxy
from src.utils import Utils
import json
import os
import matplotlib.pyplot as plt
import numpy as np
class Source(AbstractProxy):
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Inicializa a source de mensagens para alimentação ou validação do modelo.

        Args:
            config: Dicionário de configuração com parâmetros necessários
        """
        super().__init__()
        self.etapa_alimentacao_modelo: bool = config.get("etapa_alimentacao_modelo", False)
        self.atraso_chegada: int = config.get("atraso_chegada", 0)  # em ms
        self.max_mensagens_esperadas: int = config.get("max_mensagens_esperadas", 30)
        self.contador_mensagem_atual: int = 0
        self.qtd_servicos: List[int] = config.get("qtd_servicos", [])  # Ex: [1, 2] N de serviços por LB
        self.tempos_resposta: List[float] = []  # MRTs
        self.tempos_conexao: List[float] = []   # Tempo de conexão TCP

        enderecos_lb_str = config.get("enderecos_load_balancers", "")

        self.tempos_resposta: List[float] = []  # Armazena MRTs calculados

        self.ip_destino: str = config.get("ip_destino", "loadbalance1")
        self.porta_destino: int = config.get("porta_destino", 2000)

        self.log(f"Source iniciando. Etapa alimentação: {self.etapa_alimentacao_modelo}")
        self.log(f"Destino para alimentação: {self.ip_destino}:{self.porta_destino}")
        self.log(f"Endereços dos LBs para validação: {enderecos_lb_str}")
        self.log(f"Qtd serviços por ciclo validação: {self.qtd_servicos}")
        self.log(f"Atraso entre mensagens: {self.atraso_chegada} ms")
        self.log(f"Máx mensagens por ciclo: {self.max_mensagens_esperadas}")

        # Parse dos endereços dos Load Balancers
        if isinstance(enderecos_lb_str, str) and enderecos_lb_str:
            self.enderecos_lb: List[Tuple[str, int]] = []
            try:
                for endereco in enderecos_lb_str.split(","):
                    ip, porta_str = endereco.strip().split(":")
                    self.enderecos_lb.append((ip, int(porta_str)))
            except ValueError as e:
                self.log(f"ERRO ao processar enderecos_lb: '{enderecos_lb_str}'. {e}")
                self.enderecos_lb = []  # Reseta para evitar erros
        else:
            self.enderecos_lb = []
        
        if not self.enderecos_lb and not self.etapa_alimentacao_modelo:
            self.log("ALERTA: Nenhum endereço de LB configurado para validação.")

    

    def executar(self) -> None:
        """Inicia o fluxo principal da source."""
        self.log("Iniciando execução da source")
        if self.etapa_alimentacao_modelo:
            self.enviar_mensagens_alimentacao()
        else:
            if not self.enderecos_lb:
                self.log("ERRO: Validação sem LBs configurados. Abortando.")
                return
            self.enviar_mensagens_validacao()
        self.salvar_mrts_json()
        self.log("Execução da source concluída.")

    def enviar_mensagens_alimentacao(self) -> None:
        """Envia mensagens para alimentar o modelo."""
        self.log("Iniciando etapa de alimentação do modelo")
        if not self.ip_destino or not self.porta_destino:
            self.log("ERRO: IP/porta destino não configurados para alimentação.")
            return

        for i in range(self.max_mensagens_esperadas):
            msg = f"ALIMENTACAO;{self.contador_mensagem_atual};{Utils.obter_timestamp_atual()};Payload_alimentacao_{i}"
            self.log(f"Enviando mensagem: {msg} para {self.ip_destino}:{self.porta_destino}")
            
            resposta = self.enviar_e_receber(self.ip_destino, self.porta_destino, msg, eh_alimentacao=True)
            
            if resposta:
                self.log(f"Resposta recebida: {resposta}")
            else:
                self.log(f"Sem resposta para mensagem {msg}")
                
            self.contador_mensagem_atual += 1
            if self.atraso_chegada > 0:
                time.sleep(self.atraso_chegada / 1000.0)
                
        self.log("Etapa de alimentação concluída.")
    
    def enviar_mensagens_validacao(self) -> None:
        """Executa ciclos de validação com diferentes quantidades de serviços."""
        self.log("Iniciando etapa de validação")
        if not self.qtd_servicos:
            self.log("ALERTA: Nenhuma qtd_servicos definida. Sem validação.")
            return

        for ciclo_idx, num_servicos in enumerate(self.qtd_servicos):
            self.log(f">>> Iniciando Ciclo {ciclo_idx} com {num_servicos} serviço(s) <<<")
            self.contador_mensagem_atual = 1  # Reinicia contador
            self.tempos_resposta.clear()

            if not self.enderecos_lb:
                self.log(f"ERRO: Sem LBs para ciclo {ciclo_idx}. Pulando.")
                continue

            # Configura LBs para este ciclo
            msg_config = f"config;{num_servicos}"
            for lb_ip, lb_porta in self.enderecos_lb:
                self.log(f"Configurando LB {lb_ip}:{lb_porta} com '{msg_config}'")
                resposta = self.enviar_e_receber(lb_ip, lb_porta, msg_config, eh_config=True)
                if resposta:
                    self.log(f"Resposta do LB: {resposta}")

            # Envia mensagens de validação
            mensagens_enviadas = 0
            num_lbs = len(self.enderecos_lb)

            for i in range(self.max_mensagens_esperadas):
                lb_ip, lb_porta = self.enderecos_lb[i % num_lbs]
                payload = f"Dados_msg_{self.contador_mensagem_atual}_ciclo_{ciclo_idx}"
                msg = f"{ciclo_idx};{self.contador_mensagem_atual};{Utils.obter_timestamp_atual()};{payload}"
                
                self.log(f"Enviando para LB {lb_ip}:{lb_porta}: {msg}")
                self.enviar_e_receber(lb_ip, lb_porta, msg, info_ciclo=ciclo_idx)
                
                self.contador_mensagem_atual += 1
                mensagens_enviadas += 1
                if self.atraso_chegada > 0:
                    time.sleep(self.atraso_chegada / 1000.0)

            # Estatísticas do ciclo
            respostas_validas = len(self.tempos_resposta)
            mrt_medio = self.calcular_media(self.tempos_resposta) if self.tempos_resposta else 0.0
            desvio_padrao = self.calcular_desvio_padrao(self.tempos_resposta) if self.tempos_resposta else 0.0

            self.log(f"----- Ciclo {ciclo_idx} Finalizado -----")
            self.log(f"Mensagens enviadas: {mensagens_enviadas}")
            self.log(f"Respostas válidas: {respostas_validas}")
            self.log(f"MRT médio: {mrt_medio:.2f} ms")
            self.log(f"Desvio padrão: {desvio_padrao:.2f} ms")

        self.log("Etapa de validação concluída.")

    def enviar_e_receber(self, ip: str, porta: int, mensagem: str, 
                      eh_config: bool = False, 
                      eh_alimentacao: bool = False,
                      info_ciclo: Optional[int] = None) -> Optional[str]:
        resposta = None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10.0)
                
                # ⏱️ Medir tempo de conexão
                inicio_conexao = time.time()
                s.connect((ip, porta))
                fim_conexao = time.time()
                
                tempo_conexao_ms = (fim_conexao - inicio_conexao) * 1000.0
                self.tempos_conexao.append(tempo_conexao_ms)

                self.log(f"Tempo de conexão com {ip}:{porta} = {tempo_conexao_ms:.2f} ms")
                
                # Timestamp de envio
                timestamp_envio = 0.0
                if not eh_config:
                    partes = mensagem.split(";")
                    if len(partes) >= 3:
                        try:
                            timestamp_envio = float(partes[2])
                        except ValueError:
                            self.log(f"AVISO: Timestamp inválido em: {mensagem}")

                s.sendall(mensagem.encode())
                dados_recebidos = s.recv(2048)
                resposta = dados_recebidos.decode()

                # Processamento das respostas
                if eh_config:
                    self.log(f"Resposta de configuração: {resposta}")
                elif eh_alimentacao:
                    self.log(f"Resposta de alimentação: {resposta}")
                else:
                    tempo_recebimento = time.time()
                    if timestamp_envio > 0:
                        mrt_ms = (tempo_recebimento - timestamp_envio) * 1000.0
                        self.tempos_resposta.append(mrt_ms)
                        prefixo = f"[Ciclo {info_ciclo}] " if info_ciclo is not None else ""
                        self.log(f"{prefixo}MRT: {mrt_ms:.2f} ms | Resposta: {resposta}")

        except socket.timeout:
            self.log(f"TIMEOUT ao comunicar com {ip}:{porta}")
        except ConnectionRefusedError:
            self.log(f"Conexão recusada por {ip}:{porta}")
        except Exception as e:
            self.log(f"ERRO geral com {ip}:{porta}: {str(e)}")
        
        return resposta


    def salvar_mrts_json(self, nome_arquivo: str = "../resultados/resultados_mrt.json") -> None:
        resultados = {
            'total_requests': len(self.tempos_resposta),
            'successful_requests': len(self.tempos_resposta),
            'failed_requests': 0,
            'total_mrt_time': sum(self.tempos_resposta),
            'total_connection_time': sum(self.tempos_conexao),
            'requests_per_service': {},
            'cycles': []
        }

        mensagens_por_ciclo = [10, 10, 10]  # Ajuste conforme sua configuração

        total_esperado = sum(mensagens_por_ciclo)
        if len(self.tempos_resposta) != total_esperado:
            print(f"⚠️ Aviso: Número de tempos de resposta ({len(self.tempos_resposta)}) não corresponde ao esperado ({total_esperado})")
        if len(self.tempos_conexao) != total_esperado:
            print(f"⚠️ Aviso: Número de tempos de conexão ({len(self.tempos_conexao)}) não corresponde ao esperado ({total_esperado})")

        # Divide os tempos por ciclo
        tempos_resposta_por_ciclo = []
        tempos_conexao_por_ciclo = []

        inicio = 0
        for num_mensagens in mensagens_por_ciclo:
            fim = inicio + num_mensagens
            tempos_resposta_ciclo = self.tempos_resposta[inicio:fim]
            tempos_conexao_ciclo = self.tempos_conexao[inicio:fim]
            tempos_resposta_por_ciclo.append(tempos_resposta_ciclo)
            tempos_conexao_por_ciclo.append(tempos_conexao_ciclo)
            inicio = fim

        # Preenche os ciclos no JSON
        for ciclo_idx, (num_servicos, tempos_resposta_ciclo, tempos_conexao_ciclo) in enumerate(
            zip(self.qtd_servicos, tempos_resposta_por_ciclo, tempos_conexao_por_ciclo)):

            resultados['cycles'].append({
                'cycle_index': ciclo_idx,
                'num_services': num_servicos,
                'messages_sent': len(tempos_resposta_ciclo),
                'valid_responses': len(tempos_resposta_ciclo),
                'mrt_media_ms': self.calcular_media(tempos_resposta_ciclo) if tempos_resposta_ciclo else 0.0,
                'desvio_padrao_mrt_ms': self.calcular_desvio_padrao(tempos_resposta_ciclo) if tempos_resposta_ciclo else 0.0,
                'connection_media_ms': self.calcular_media(tempos_conexao_ciclo) if tempos_conexao_ciclo else 0.0,
                'desvio_padrao_conexao_ms': self.calcular_desvio_padrao(tempos_conexao_ciclo) if tempos_conexao_ciclo else 0.0,
                'tempos_mrt_ms': tempos_resposta_ciclo,
                'tempos_conexao_ms': tempos_conexao_ciclo
            })

        # Inclui todos os tempos brutos no topo do JSON
        resultados['all_tempos_mrt_ms'] = self.tempos_resposta
        resultados['all_tempos_conexao_ms'] = self.tempos_conexao

        # Garante que o diretório existe
        import os
        os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
        
        # Salva no arquivo JSON
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=4)

        print(f"\nResultados salvos em {nome_arquivo}")
        self.gerar_graficos_mrt()


    def gerar_graficos_mrt(self, nome_arquivo: str = "../graphs/resultados_mrt.png") -> None:
        """Gera gráficos de MRT vs Número de Serviços e MRT vs Taxa de Geração."""
        if not self.tempos_resposta:
            self.log("Sem dados para gerar gráficos")
            return

        # Prepara os dados para o primeiro gráfico (MRT vs Número de Serviços)
        dados_mrt_servicos = []
        inicio = 0
        for ciclo_idx, num_servicos in enumerate(self.qtd_servicos):
            fim = inicio + self.max_mensagens_esperadas
            tempos_ciclo = self.tempos_resposta[inicio:fim]
            if tempos_ciclo:
                mrt_medio = self.calcular_media(tempos_ciclo)
                dados_mrt_servicos.append((num_servicos, mrt_medio))
            inicio = fim

        # Gera o primeiro gráfico (MRT vs Número de Serviços)
        plt.figure(figsize=(10, 6))
        num_servicos = [item[0] for item in dados_mrt_servicos]
        avg_mrts = [item[1] for item in dados_mrt_servicos]
        
        plt.plot(num_servicos, avg_mrts, marker='o', linestyle='-')
        plt.title('Tempo Médio de Resposta (MRT) vs. Número de Serviços')
        plt.xlabel("Número de Serviços no Ciclo")
        plt.ylabel("Tempo Médio de Resposta (MRT) (ms)")
        plt.xticks(num_servicos)
        plt.grid(True, which="both", ls="--")
        plt.tight_layout()
        
        # Salva o primeiro gráfico
        nome_arquivo_mrt = nome_arquivo.replace('.png', '_mrt_vs_num_servicos.png')
        plt.savefig(nome_arquivo_mrt)
        self.log(f"Gráfico MRT vs Número de Serviços salvo em: {nome_arquivo_mrt}")

        # Prepara os dados para o segundo gráfico (MRT vs Taxa de Geração)
        arrival_delays = [7500, 5000, 2000, 1000, 500, 250]  # Taxas de chegada crescentes
        real_arrival_delay = self.atraso_chegada if self.atraso_chegada > 0 else 2000

        experimental_data = {}
        for delay in arrival_delays:
            fator = real_arrival_delay / delay
            experimental_data[delay] = [(s, mrt * fator) for s, mrt in dados_mrt_servicos]

        # Gera o segundo gráfico (MRT vs Taxa de Geração)
        plt.figure(figsize=(12, 7))
        
        all_num_services = sorted(list(set(
            item[0] for delay_data in experimental_data.values() for item in delay_data
        )))

        for num_s in all_num_services:
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
                plt.plot(rates_sorted, mrts_sorted, marker='o', linestyle='-', label=f'{num_s} Serviço(s)')

        plt.title('Tempo Médio de Resposta (MRT) vs. Taxa de Geração de Mensagens')
        plt.xlabel("Taxa de Geração de Mensagens (mensagens/segundo)")
        plt.ylabel("Tempo Médio de Resposta (MRT) (ms)")
        if any(all_num_services):
            plt.legend(title="Número de Serviços")
        plt.grid(True, which="both", ls="--")
        plt.tight_layout()

        # Salva o segundo gráfico
        nome_arquivo_taxa = nome_arquivo.replace('.png', '_mrt_vs_taxa_geracao.png')
        plt.savefig(nome_arquivo_taxa)
        self.log(f"Gráfico MRT vs Taxa de Geração salvo em: {nome_arquivo_taxa}")

        plt.close('all')  # Fecha todas as figuras para liberar memória

    @staticmethod
    def calcular_media(valores: List[float]) -> float:
        """Calcula a média de uma lista de valores."""
        return sum(valores) / len(valores) if valores else 0.0

    @staticmethod
    def calcular_desvio_padrao(valores: List[float]) -> float:
        """Calcula o desvio padrão amostral de uma lista de valores."""
        if not valores or len(valores) < 2:
            return 0.0
            
        media = Source.calcular_media(valores)
        variancia = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
        return variancia ** 0.5