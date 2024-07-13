from enum import Enum


class ResonatorEnum(str, Enum):
    LEVEL: str = "等級"
    HP: str = "生命"
    ATK: str = "攻擊"
    DEF: str = "防禦"
