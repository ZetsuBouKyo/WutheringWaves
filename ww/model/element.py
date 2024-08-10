from enum import Enum

from ww.locale import ZhTwEnum, _


class ElementEnum(str, Enum):
    GLACIO: str = _(ZhTwEnum.GLACIO)
    FUSION: str = _(ZhTwEnum.FUSION)
    ELECTRO: str = _(ZhTwEnum.ELECTRO)
    AERO: str = _(ZhTwEnum.AERO)
    SPECTRO: str = _(ZhTwEnum.SPECTRO)
    HAVOC: str = _(ZhTwEnum.HAVOC)
