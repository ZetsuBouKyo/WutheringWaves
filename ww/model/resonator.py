from enum import Enum

from ww.locale import ZhHantEnum, _


class ResonatorEnum(str, Enum):
    LEVEL: str = _(ZhHantEnum.LEVEL)
    HP: str = _(ZhHantEnum.HP)
    ATK: str = _(ZhHantEnum.ATK)
    DEF: str = _(ZhHantEnum.DEF)


class ResonatorBuffEnum(str, Enum):
    CHAIN: str = "共鳴鏈"
    INHERENT_SKILL: str = "固有"
    OUTRO: str = "延奏"
    SKILL: str = "技能"
