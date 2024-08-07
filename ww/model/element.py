from enum import Enum

from ww.locale import ZhHantEnum, _


class ElementEnum(str, Enum):
    GLACIO: str = _(ZhHantEnum.GLACIO)
    FUSION: str = _(ZhHantEnum.FUSION)
    ELECTRO: str = _(ZhHantEnum.ELECTRO)
    AERO: str = _(ZhHantEnum.AERO)
    SPECTRO: str = _(ZhHantEnum.SPECTRO)
    HAVOC: str = _(ZhHantEnum.HAVOC)
