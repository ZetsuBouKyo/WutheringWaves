from decimal import Decimal
from enum import Enum
from typing import Union

from ww.locale import ZhTwEnum, _

Number = Union[float, int, str, Decimal]


class SkillBaseAttrEnum(str, Enum):
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)
