import socket
import datetime
import time
from typing import List, Dict, Any, Optional, Tuple
from src.abstract_proxy import AbstractProxy
from src.utils import Utils
import json
from src.graficos import gerar_graficos_mrt
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
        self.max_mensagens_esperadas: int = config.get("max_mensagens_esperadas", 10)
        self.contador_mensagem_atual: int = 0
        self.qtd_servicos: List[int] = config.get("qtd_servicos", [])  # Ex: [1, 2] N de serviços por LB

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
        """
        Método unificado para envio e recebimento com tratamento de erros.
        
        Args:
            ip: IP de destino
            porta: Porta de destino
            mensagem: Conteúdo a ser enviado
            eh_config: Se é mensagem de configuração
            eh_alimentacao: Se é mensagem de alimentação
            info_ciclo: Número do ciclo atual (para logs)
            
        Returns:
            Resposta recebida ou None em caso de erro
        """
        resposta = None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10.0)
                s.connect((ip, porta))
                
                # Extrai timestamp de envio se aplicável
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

                # Processa resposta conforme tipo de mensagem
                if eh_config:
                    self.log(f"Resposta de configuração: {resposta}")
                elif eh_alimentacao:
                    self.log(f"Resposta de alimentação: {resposta}")
                else:  # Mensagem de validação
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
            'total_requests': self.contador_mensagem_atual - 1,
            'successful_requests': len(self.tempos_resposta),
            'failed_requests': (self.contador_mensagem_atual - 1) - len(self.tempos_resposta),
            'total_time': sum(self.tempos_resposta),
            'requests_per_service': {},
            'cycles': []
        }

        if not self.etapa_alimentacao_modelo:
            for ciclo_idx, num_servicos in enumerate(self.qtd_servicos):
                respostas_ciclo = self.tempos_resposta[
                    ciclo_idx * self.max_mensagens_esperadas:
                    (ciclo_idx + 1) * self.max_mensagens_esperadas
                ]

                mrt_medio = self.calcular_media(respostas_ciclo) if respostas_ciclo else 0.0
                desvio = self.calcular_desvio_padrao(respostas_ciclo) if respostas_ciclo else 0.0

                resultados['cycles'].append({
                    'cycle_index': ciclo_idx,
                    'num_services': num_servicos,
                    'messages_sent': self.max_mensagens_esperadas,
                    'valid_responses': len(respostas_ciclo),
                    'mrt_media_ms': mrt_medio,
                    'desvio_padrao_ms': desvio,
                    'tempos_ms': respostas_ciclo
                })
        else:
            resultados['cycles'].append({
                'cycle_index': 0,
                'alimentacao': True,
                'messages_sent': self.max_mensagens_esperadas,
                'valid_responses': len(self.tempos_resposta),
                'tempos_ms': self.tempos_resposta
            })

        # Garante que o diretório existe
        import os
        os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
        
        # Salva no arquivo JSON
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=4)

        print(f"\nResultados salvos em {nome_arquivo}")
        
        # Chama a função de gráficos passando o arquivo correto
        self.gerar_graficos_mrt(nome_arquivo)
        self.log("Passou pelos graficos")


    def gerar_graficos_mrt(self, nome_arquivo: str):
        self.log(f"Entrou aqui!!!!!!")
        """Gera gráficos a partir do JSON e salva no mesmo diretório"""
        try:
            self.log(f"Entrou aqui")
            import matplotlib
            # Força o backend 'Agg' que funciona em containers sem display
            matplotlib.use('Agg')

            # Obtém o diretório do arquivo JSON
            output_dir = os.path.dirname(nome_arquivo)
            
            # Verifica se o diretório existe
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                self.log(f"Diretório {output_dir} criado")

            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            if not dados['cycles']:
                self.log("Nenhum dado para gerar gráficos")
                return

            # Gráfico 1 - MRT por serviço
            plt.figure(figsize=(10, 6))
            for ciclo in dados['cycles']:
                if not ciclo.get('alimentacao', False):
                    plt.plot(ciclo['tempos_ms'], 
                            label=f"{ciclo['num_services']} serviço(s)")
            
            plt.title("Tempos de Resposta por Serviço")
            plt.xlabel("Requisição")
            plt.ylabel("MRT (ms)")
            plt.legend()
            plt.grid(True)
            
            graph1_path = os.path.join(output_dir, "mrt_por_servico.png")
            plt.savefig(graph1_path)
            plt.close()
            self.log(f"Gráfico 1 salvo em {graph1_path}")

            # Gráfico 2 - Evolução temporal
            plt.figure(figsize=(12, 6))
            for ciclo in dados['cycles']:
                if not ciclo.get('alimentacao', False):
                    mrt_medio = ciclo['mrt_media_ms']
                    plt.scatter(ciclo['cycle_index'], mrt_medio,
                            label=f"{ciclo['num_services']} serviço(s)")
            
            plt.title("MRT Médio por Ciclo")
            plt.xlabel("Ciclo")
            plt.ylabel("MRT Médio (ms)")
            plt.legend()
            plt.grid(True)
            
            graph2_path = os.path.join(output_dir, "mrt_evolucao.png")
            plt.savefig(graph2_path)
            plt.close()
            self.log(f"Gráfico 2 salvo em {graph2_path}")

        except Exception as e:
            self.log(f"Falha ao gerar gráficos: {str(e)}")

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