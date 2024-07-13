from enum import Enum


class MonsterEnum(str, Enum):
    NAME: str = "怪物名稱"
    LEVEL: str = "等級"
    DEF: str = "防禦"

    PHYSICAL_DMG_RES = "物理抗性"
    GLACIO_DMG_RES = "冷凝抗性"
    FUSION_DMG_RES = "熱熔抗性"
    ELECTRO_DMG_RES = "導電抗性"
    AERO_DMG_RES = "氣動抗性"
    SPECTRO_DMG_RES = "衍射抗性"
    HAVOC_DMG_RES = "湮滅抗性"
