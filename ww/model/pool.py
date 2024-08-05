from enum import Enum


class GachaPoolTypeEnum(str, Enum):
    FEATURED_RESONATOR_CONVENE: str = "角色活動喚取"
    FEATURED_WEAPON_CONVENE: str = "武器活動喚取"
    STANDARD_RESONATOR_CONVENE: str = "角色常駐喚取"
    STANDARD_WEAPON_CONVENE: str = "武器常駐喚取"
