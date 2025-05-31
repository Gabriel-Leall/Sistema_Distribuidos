from src.load_balancer_proxy import LoadBalancerProxy
from src.service_proxy import ServiceProxy
from src.source import Source
from src.config import configuracao
from typing import Optional, List, Tuple
import sys

def parsear_enderecos_services(enderecos_str: str) -> List[Tuple[str, int]]:
    """
    Converte string de endereços para lista de tuplas (ip, porta).
    
    Args:
        enderecos_str: Formato "ip1:porta1,ip2:porta2"
        
    Returns:
        Lista de tuplas (ip, porta)
        
    Raises:
        ValueError: Se formato for inválido
    """
    enderecos = []
    for par in enderecos_str.split(','):
        if ':' not in par:
            raise ValueError(f"Formato inválido: '{par}'")
        ip, porta = par.split(':', 1)
        enderecos.append((ip.strip(), int(porta.strip())))
    return enderecos

def iniciar_Source(config: Optional[dict] = None) -> None:
    """
    Inicia a source para alimentação e validação do modelo.
    
    Args:
        config: Dicionário de configuração. Se None, carrega do arquivo.
    """
    if configuracao is None:
        configuracao = config()
    print("Configuração carregada para source:", config)

    # Etapa de alimentação
    print("\n=== ETAPA DE ALIMENTAÇÃO DO MODELO ===")
    config_alimentacao = config.copy()
    config_alimentacao["etapa_alimentacao_modelo"] = True
    
    if config_alimentacao.get("habilitar_alimentacao", True):
        source_alimentacao = Source(config_alimentacao)
        source_alimentacao.executar()
    else:
        print("Etapa de alimentação desabilitada na configuração")

    # Etapa de validação
    print("\n=== ETAPA DE VALIDAÇÃO ===")
    config_validacao = config.copy()
    config_validacao["etapa_alimentacao_modelo"] = False
    
    if config_validacao.get("habilitar_validacao", True):
        source_validacao = Source(config_validacao)
        source_validacao.executar()
    else:
        print("Etapa de validação desabilitada na configuração")

def iniciar_balanceador(porta_escuta: int = 2000, 
                       enderecos_services_str: Optional[str] = None) -> None:
    """
    Inicia um balanceador de carga.
    
    Args:
        porta_escuta: Porta para escutar conexões
        enderecos_services_str: String com endereços dos serviços backend
    """
    try:
        enderecos_services = []
        if enderecos_services_str:
            enderecos_services = parsear_enderecos_services(enderecos_services_str)
        
        print(f"\nIniciando Balanceador na porta {porta_escuta}")
        print(f"Serviços backend: {enderecos_services or 'Nenhum'}")
        
        balanceador = LoadBalancerProxy(porta_escuta=porta_escuta, 
                                     enderecos_services=enderecos_services)
        balanceador.iniciar()
    except ValueError as e:
        print(f"ERRO: {e}")
        sys.exit(1)

def iniciar_service(porta: int, 
                   tempo_service_ms: float, 
                   nome_modelo: str) -> None:
    """
    Inicia uma instância de serviço.
    
    Args:
        porta: Porta para escutar conexões
        tempo_service_ms: Tempo simulado de serviço (ms)
        nome_modelo: Nome do modelo IA a ser usado
    """
    print(f"\nIniciando Serviço na porta {porta}")
    print(f"Modelo: {nome_modelo} | Tempo serviço: {tempo_service_ms}ms")
    
    service = ServiceProxy(porta_escuta=porta,
                     tempo_service_ms=tempo_service_ms,
                     nome_modelo=nome_modelo)
    service.iniciar()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    papel = sys.argv[1].lower()
    config = configuracao()

    try:
        if papel == "souce":
            iniciar_Source(config=config)

        elif papel == "lb":
            if len(sys.argv) < 4:
                print("Erro: argumentos insuficientes para balanceador")
        
                sys.exit(1)
                
            porta = int(sys.argv[2])
            enderecos = sys.argv[3]
            iniciar_balanceador(porta_escuta=porta, 
                              enderecos_services_str=enderecos)

        elif papel == "service":
            if len(sys.argv) < 5:
                print("Erro: argumentos insuficientes para serviço")
                sys.exit(1)
                
            porta = int(sys.argv[2])
            tempo_service = float(sys.argv[3])
            modelo = sys.argv[4]
            iniciar_service(porta=porta,
                          tempo_service_ms=tempo_service,
                          nome_modelo=modelo)

        else:
            print(f"Função desconhecida: {papel}")
            sys.exit(1)

    except ValueError as e:
        print(f"Erro nos argumentos: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)