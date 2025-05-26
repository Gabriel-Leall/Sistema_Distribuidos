class TargetAddress:
    def __init__(self, host: str, port: int, service_time: float = 0.0, std: float = 0.0):
        self.host = host
        self.port = port
        self.service_time = service_time
        self.std = std 