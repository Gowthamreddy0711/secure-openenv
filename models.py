from dataclasses import dataclass

@dataclass
class SecureAction:
    increase_encryption: bool
    block_users: int
    allocate_resources: int
    activate_firewall: bool

@dataclass
class SecureObservation:
    active_users: int
    attack_level: float
    server_load: float
    encryption_level: int
    threat_type: str
    reward: float
    done: bool

@dataclass
class SecureState:
    step_count: int
    total_breaches: int
