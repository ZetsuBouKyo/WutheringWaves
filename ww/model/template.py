from enum import Enum
from typing import List

from pydantic import BaseModel


class TemplateEnum(str, Enum):
    RESONATOR_NAME: str = "[角色]名稱"
    REAL_DMG_NO_CRIT: str = "[實戰]無暴擊"
    REAL_DMG_CRIT: str = "[實戰]暴擊"
    ACTION: str = "[實戰]操作"
    SKILL_ID: str = "[實戰]技能代稱"
    BONUS_TYPE: str = "[實戰]技能加成種類"
    BONUS_MAGNIFIER: str = "[額外]倍率"
    BONUS_AMPLIFIER: str = "[額外]加深"
    BONUS_ATK_P: str = "[額外]攻擊百分比"
    BONUS_ATK: str = "[額外]攻擊"
    BONUS_CRIT_RATE: str = "[額外]暴擊"
    BONUS_CRIT_DMG: str = "[額外]暴擊傷害"
    BONUS_ADDITION: str = "[額外]加成"
    BONUS_SKILL_DMG_ADDITION: str = "[額外]招式倍率"
    BONUS_IGNORE_DEF: str = "[額外]忽視防禦"
    BONUS_REDUCE_RES: str = "[額外]抗性降低"
    RESONATING_SPIN_CONCERTO_REGEN: str = "協奏能量"
    ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN: str = "累積協奏"
    TIME_START: str = "[實戰]起手秒數"
    TIME_END: str = "[實戰]結束秒數"
    CUMULATIVE_TIME: str = "[實戰]累積結束秒數"
    FRAME: str = "幀數"


class CalculatedTemplateEnum(str, Enum):
    RESONATOR_NAME: str = "[角色]名稱"
    SKILL_ID: str = "[操作]技能代稱"

    RESONATOR_SKILL_LEVEL: str = "[角色技能]等級"
    RESONATOR_SKILL_ELEMENT: str = "[角色技能]屬性"
    RESONATOR_SKILL_BASE_ATTR: str = "[角色技能]基礎參數"
    RESONATOR_SKILL_TYPE: str = "[角色技能]種類"
    RESONATOR_SKILL_TYPE_BONUS: str = "[角色技能]加成種類"
    RESONATOR_SKILL_DMG: str = "[角色技能]倍率"

    ECHO_ELEMENT: str = "[聲骸]屬性"
    ECHO_SKILL_DMG: str = "[聲骸]技能倍率"

    MONSTER_LEVEL: str = "[怪物]等級"
    MONSTER_DEF: str = "[怪物]防禦"
    MONSTER_RES: str = "[怪物]抗性"

    FINAL_ATK: str = "[總]攻擊"
    FINAL_ATK_ADDITION: str = "[總]額外攻擊"
    FINAL_ATK_P: str = "[總]攻擊百分比"
    FINAL_CRIT_RATE: str = "[總]暴擊"
    FINAL_CRIT_DMG: str = "[總]暴擊傷害"
    FINAL_BONUS: str = "[總]加成區百分比"

    FINAL_ELEMENT: str = "[總]屬性"
    FINAL_BONUS_TYPE: str = "[總]加成種類"
    FINAL_SKILL_DMG: str = "[總]技能倍率"

    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"


class TemplateRowModel(BaseModel):
    resonator_name: str = ""


class TemplateModel(BaseModel):
    resonator_1_name: str = ""
    resonator_1_chain: str = ""
    resonator_1_weapon_name: str = ""
    resonator_1_weapon_rank: str = ""

    resonator_2_name: str = ""
    resonator_2_chain: str = ""
    resonator_2_weapon_name: str = ""
    resonator_2_weapon_rank: str = ""

    resonator_3_name: str = ""
    resonator_3_chain: str = ""
    resonator_3_weapon_name: str = ""
    resonator_3_weapon_rank: str = ""

    title_prefix: str = ""
    title_suffix: str = ""
    monster_id: str = ""
    description: str = ""

    rows: List[TemplateRowModel] = []
