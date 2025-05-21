class TargetAddress:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def get_ip(self) -> str:
        return self.ip

    def get_port(self) -> int:
        return self.port
