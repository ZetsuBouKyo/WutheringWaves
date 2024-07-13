from enum import Enum


class WeaponStatEnum(str, Enum):
    LEVEL: str = "等級"
    ATK: str = "攻擊"
    ATK_P: str = "攻擊百分比"
    DEF_P: str = "防禦百分比"
    HP_P: str = "生命百分比"
    CRIT_DMG: str = "暴擊傷害"
    CRIT_RATE: str = "暴擊"
    ENERGY_REGEN: str = "共鳴效率"


class WeaponRankEnum(str, Enum):
    LEVEL: str = "等級"
    ATK_P: str = "攻擊提升"
    ATTRIBUTE_DMG_BONUS: str = "全屬性傷害加成提升"
    ENERGY_REGEN: str = "共鳴效率提升"
