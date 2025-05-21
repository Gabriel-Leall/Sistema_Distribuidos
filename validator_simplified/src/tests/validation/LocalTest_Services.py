from LoadBalancerProxy import LoadBalancerProxy
from Source import Source

# Estes estudos de caso são apenas ilustrativos e de testes.
# Estes estudos de caso não devem ser executados da maneira que está aqui (monolítico).
# Você deve executar os componentes separadamente de forma distribuída em máquinas físicas ou VMs e contêineres.

def execute_stage():
    path = "src/tests/validation/"
    load_balancer_json_path1 = f"{path}loadbalancer1.properties"
    load_balancer_json_path2 = f"{path}loadbalancer2.properties"

    # Inicia os proxies do balanceador de carga
    LoadBalancerProxy(load_balancer_json_path2).start()
    LoadBalancerProxy(load_balancer_json_path1).start()

    # Inicia a fonte
    Source(path).start()

if __name__ == "__main__":
    execute_stage()

