from enum import Enum

class VariatedParameter(Enum):
    SERVICES = "Services"
    AR = "AR"

    @classmethod
    def from_value(cls, value: str):
        for param in cls:
            if param.value.lower() == value.lower():
                return param
        raise ValueError(f"Invalid variatedParameter value: {value}")