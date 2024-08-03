from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

TEMPLATE_BONUS = "[額外]"


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

    MONSTER_LEVEL: str = "[怪物]等級"
    MONSTER_DEF: str = "[怪物]防禦"
    MONSTER_RES: str = "[怪物]抗性"


class TemplateResonatorEnum(str, Enum):
    RESONATOR_NAME: str = "[角色]名稱"
    RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    RESONATOR_WEAPON_NAME: str = "[武器]名稱"
    RESONATOR_WEAPON_RANK: str = "[武器]諧振"
    RESONATOR_INHERENT_SKILL_1: bool = "[角色]固有1"
    RESONATOR_INHERENT_SKILL_2: bool = "[角色]固有2"
    RESONATOR_ECHO_1: str = "[聲骸]名稱"
    RESONATOR_ECHO_SONATA_1: str = "[聲骸]合鳴1"
    RESONATOR_ECHO_SONATA_2: str = "[聲骸]合鳴2"
    RESONATOR_ECHO_SONATA_3: str = "[聲骸]合鳴3"
    RESONATOR_ECHO_SONATA_4: str = "[聲骸]合鳴4"
    RESONATOR_ECHO_SONATA_5: str = "[聲骸]合鳴5"


class TemplateResonatorModel(BaseModel):
    resonator_name: str = ""
    resonator_chain: str = ""
    resonator_weapon_name: str = ""
    resonator_weapon_rank: str = ""
    resonator_inherent_skill_1: bool = None
    resonator_inherent_skill_2: bool = None
    resonator_echo_1: str = ""
    resonator_echo_sonata_1: str = ""
    resonator_echo_sonata_2: str = ""
    resonator_echo_sonata_3: str = ""
    resonator_echo_sonata_4: str = ""
    resonator_echo_sonata_5: str = ""


class TemplateRowBuffTypeEnum(str, Enum):
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


class TemplateRowEnum(str, Enum):
    BONUS_BUFF: str = "增益"
    RESONATOR_NAME: str = "[角色]名稱"
    REAL_DMG_NO_CRIT: str = "[實戰]無暴擊"
    REAL_DMG_CRIT: str = "[實戰]暴擊"
    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"
    ACTION: str = "[實戰]操作"
    SKILL_ID: str = "[實戰]技能代稱"
    SKILL_BONUS_TYPE: str = "[實戰]技能加成種類"
    BONUS_MAGNIFIER: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.MAGNIFIER.value}"
    BONUS_AMPLIFIER: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.AMPLIFIER.value}"
    BONUS_HP_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.HP_P.value}"
    BONUS_HP: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.HP.value}"
    BONUS_ATK_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ATK_P.value}"
    BONUS_ATK: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ATK.value}"
    BONUS_DEF_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.DEF_P.value}"
    BONUS_DEF: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.DEF.value}"
    BONUS_CRIT_RATE: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.CRIT_RATE.value}"
    BONUS_CRIT_DMG: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.CRIT_DMG.value}"
    BONUS_ADDITION: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ADDITION.value}"
    BONUS_SKILL_DMG_ADDITION: str = (
        f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.SKILL_DMG_ADDITION.value}"
    )
    BONUS_IGNORE_DEF: str = (
        f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.IGNORE_DEF.value}"
    )
    BONUS_REDUCE_RES: str = (
        f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.REDUCE_RES.value}"
    )
    RESONATING_SPIN_CONCERTO_REGEN: str = "協奏能量"
    ACCUMULATED_RESONATING_SPIN_CONCERTO_REGEN: str = "累積協奏"
    TIME_START: str = "[實戰]起手秒數"
    TIME_END: str = "[實戰]結束秒數"
    CUMULATIVE_TIME: str = "[實戰]累積結束秒數"
    FRAME: str = "幀數"


class TemplateRowActionEnum(str, Enum):
    ATTACK: str = "普攻"
    ATTACK_N: str = "普攻xN"
    HEAVY_ATTACK: str = "重擊"
    RESONANCE_SKILL: str = "共鳴技能"
    RESONANCE_LIBERATION: str = "共鳴解放"
    ECHO: str = "聲骸"
    OUTRO: str = "延奏"
    INTRO: str = "變奏"
    SWITCH: str = "入場"
    SWITCH_AIR: str = "空中入場"
    GRAPPLE: str = "鉤索"
    COORDINATED_ATTACK: str = "協同攻擊"
    NONE: str = "無"


class TemplateRowBuffEnum(str, Enum):
    NAME: str = "名稱"
    TYPE: str = "種類"
    VALUE: str = "數值"
    STACK: str = "層數"
    DURATION: str = "持續時間(s)"


class TemplateRowBuffModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    type: Union[TemplateRowBuffTypeEnum, str] = ""
    value: str = ""
    stack: str = ""
    duration: str = ""

    @field_validator("type")
    @classmethod
    def name_must_contain_space(cls, v: Optional[str]) -> str:
        if v not in TemplateRowBuffTypeEnum._value2member_map_:
            return ""
        return v


class TemplateRowModel(BaseModel):
    resonator_name: str = ""
    real_dmg_no_crit: str = ""
    real_dmg_crit: str = ""
    action: str = ""
    skill_id: str = ""
    skill_bonus_type: str = ""
    buffs: List[TemplateRowBuffModel] = []
    resonating_spin_concerto_regen: str = ""
    accumulated_resonating_spin_concerto_regen: str = ""
    time_start: str = ""
    time_end: str = ""
    cumulative_time: str = ""
    frame: str = ""


class TemplateModel(BaseModel):
    id: str = ""

    test_resonator_id_1: str = ""
    test_resonator_id_2: str = ""
    test_resonator_id_3: str = ""

    monster_id: str = ""
    description: str = ""

    resonators: List[TemplateResonatorModel] = []
    rows: List[TemplateRowModel] = []
