from enum import Enum

from ww.locale import ZhTwEnum, _


class ResonatorStatEnum(str, Enum):
    LEVEL: str = _(ZhTwEnum.LEVEL)
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)


class ResonatorBuffEnum(str, Enum):
    CHAIN: str = "共鳴鏈"
    INHERENT_SKILL: str = "固有"
    OUTRO: str = "延奏"
    SKILL: str = "技能"
