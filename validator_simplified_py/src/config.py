# Configuração dos Balanceadores de Carga

BALANCER1 = {
    'name': 'Server1',
    'port': 2000,
    'num_services': 4,
    'service_time': 100.0,
    'std': 2.0,
    'is_source': False,
    'queue_size': 100
}

BALANCER2 = {
    'name': 'Server2',
    'port': 3000,
    'num_services': 4,
    'service_time': 2000.0,
    'std': 2.0,
    'is_source': True,
    'queue_size': 100
}

# Configuração dos Serviços
SERVICE_CONFIG = {
    'target_ip': 'localhost',
    'target_port': 1000
} 