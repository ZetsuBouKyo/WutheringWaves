from enum import Enum


class ElementEnum(str, Enum):
    GLACIO: str = "冷凝"
    FUSION: str = "熱熔"
    ELECTRO: str = "導電"
    AERO: str = "氣動"
    SPECTRO: str = "衍射"
    HAVOC: str = "湮滅"
