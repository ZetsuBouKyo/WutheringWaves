from enum import Enum

from ww.locale.zh_hant import ZhHantEnum

__all__ = ["ZhHantEnum"]


def get_text(text: str) -> str:
    if type(text) == str:
        return text
    elif isinstance(text, Enum):
        return text.value
    return text


_ = get_text
