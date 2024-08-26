from enum import Enum

from ww.locale import ZhTwEnum, _


class TemplateLabelTableColumnEnum(str, Enum):
    NAME: str = _(ZhTwEnum.NAME)
    DURATION_1: str = _(ZhTwEnum.DURATION_1)
    DURATION_2: str = _(ZhTwEnum.DURATION_2)
