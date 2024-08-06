from enum import Enum


class ZhHantEnum(str, Enum):
    CALCULATE: str = "計算"

    MAGNIFIER: str = "倍率"
    AMPLIFIER: str = "加深"
    HP_P: str = "生命百分比"
    HP: str = "生命"
    ATK_P: str = "攻擊百分比"
    ATK: str = "攻擊"
    DEF_P: str = "防禦百分比"
    DEF: str = "防禦"
    CRIT_RATE: str = "暴擊"
    CRIT_DMG: str = "暴擊傷害"
    ADDITION: str = "加成"
    SKILL_DMG_ADDITION: str = "招式倍率"
    IGNORE_DEF: str = "忽視防禦"
    REDUCE_RES: str = "抗性降低"

    NORMAL_ATTACK: str = "常態攻擊"
    RESONANCE_SKILL: str = "共鳴技能"
    RESONANCE_LIBERATION: str = "共鳴解放"
    INTRO_SKILL: str = "變奏技能"
    OUTRO_SKILL: str = "延奏技能"
    FORTE_CIRCUIT: str = "共鳴回路"

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
