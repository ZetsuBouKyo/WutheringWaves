from enum import Enum
from typing import Union

from ww.locale.zh_hant import ZhTwEnum

__all__ = ["ZhTwEnum"]


def get_text(text: Union[str, Enum]) -> str:
    if type(text) == str:
        return text
    elif isinstance(text, Enum):
        return text.value
    return text


_ = get_text
