from enum import Enum


class ZhHantEnum(str, Enum):
    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"

    FINAL_ELEMENT: str = "[總]屬性"
    FINAL_BONUS_TYPE: str = "[總]加成種類"
    FINAL_SKILL_DMG: str = "[總]技能倍率"

    FINAL_ATK: str = "[總]攻擊"
    FINAL_ATK_ADDITION: str = "[總]額外攻擊"
    FINAL_ATK_P: str = "[總]攻擊百分比"
    FINAL_CRIT_RATE: str = "[總]暴擊"
    FINAL_CRIT_DMG: str = "[總]暴擊傷害"
    FINAL_BONUS: str = "[總]加成區百分比"
