from typing import Dict, Any

def configuracao() -> Dict[str, Any]:
    return {
        'model_feeding_stage_enabled': True,  
        'validation_stage_enabled': True,    
        'model_feeding_stage': False, 
        'source_port': 1000,
        'target_ip': 'loadbalance1', 
        'target_port': 2000,         
        'max_considered_messages_expected': 10, 
        'arrival_delay': 100,
        'qtd_services': [1, 2], 
        'loadbalancer_addresses': 'loadbalance1:2000,loadbalance2:3000' 
    }