from enum import Enum


class ResonatorEnum(str, Enum):
    LEVEL: str = "等級"
    HP: str = "生命"
    ATK: str = "攻擊"
    DEF: str = "防禦"


class ResonatorBuffEnum(str, Enum):
    CHAIN: str = "共鳴鏈"
    INHERENT_SKILL: str = "固有"
    OUTRO: str = "延奏"
    SKILL: str = "技能"
