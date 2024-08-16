from enum import Enum

from ww.locale import ZhTwEnum, _


class SkillBaseAttrEnum(str, Enum):
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)
