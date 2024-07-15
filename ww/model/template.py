from enum import Enum


class TemplateEnum(str, Enum):
    RESONATOR_NAME: str = "角色名稱"
    REAL_DMG_NO_CRIT: str = "無暴擊"
    REAL_DMG_CRIT: str = "暴擊"
    ACTION: str = "操作"
    SKILL_ID: str = "代稱"
    BONUS_TYPE: str = "加成種類"
    BONUS_MAGNIFIER: str = "倍率"
    BONUS_AMPLIFIER: str = "加深"
    BONUS_ATK_P: str = "攻擊%"
    BONUS_ATK: str = "攻擊"
    BONUS_CRIT_RATE: str = "暴擊"
    BONUS_CRIT_DMG: str = "暴擊傷害"
    BONUS_ADDITION: str = "加成"
    BONUS_SKILL_DMG_P: str = "招式倍率(加區)"
    BONUS_IGNORE_DEF: str = "忽視防禦"
    BONUS_REDUCE_RES: str = "抗性降低"
    RESONATING_SPIN_CONCERTO_REGEN: str = "協奏能量"
    ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN: str = "累積協奏"
    TIME_START: str = "起手秒數"
    TIME_END: str = "結束秒數"
    CUMULATIVE_TIME: str = "累積結束秒數"
    FRAME: str = "幀數"


class CalculatedTemplateEnum(str, Enum):
    RESONATOR_NAME: str = "角色名稱"
    SKILL_ID: str = "技能代稱"

    RESONATOR_SKILL_LEVEL: str = "角色技能等級"
    RESONATOR_SKILL_ELEMENT: str = "角色技能屬性"
    RESONATOR_SKILL_TYPE: str = "角色技能種類"
    RESONATOR_SKILL_TYPE_BONUS: str = "角色技能加成種類"
    RESONATOR_SKILL_DMG: str = "角色技能倍率"

    ECHO_ELEMENT: str = "聲骸屬性"
    ECHO_TYPE_BONUS: str = "種類加成"
    ECHO_SKILL_DMG: str = "技能倍率"

    MONSTER_LEVEL: str = "怪物等級"
    MONSTER_DEF: str = "怪物防禦"
    MONSTER_RES: str = "怪物抗性"

    FINAL_ATK: str = "[總]攻擊"
    FINAL_ATK_ADDITION: str = "[總]額外攻擊"
    FINAL_ATK_P: str = "[總]攻擊百分比"
    FINAL_CRIT_RATE: str = "[總]暴擊"
    FINAL_CRIT_DMG: str = "[總]暴擊傷害"
    FINAL_BONUS: str = "[總]加成區百分比"

    FINAL_ELEMENT: str = "[總]屬性"
    FINAL_TYPE_BONUS: str = "[總]加成種類"
    FINAL_SKILL_DMG: str = "[總]技能倍率"

    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"
