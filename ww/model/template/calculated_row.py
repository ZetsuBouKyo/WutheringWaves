from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from ww.locale import ZhTwEnum, _
from ww.model import SkillBaseAttrEnum
from ww.model.buff import SkillBonusTypeEnum
from ww.model.element import ElementEnum
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.template.buff_table import TemplateBuffTableRowModel


class CalculatedTemplateColumnEnum(str, Enum):
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

    DAMAGE: str = _(ZhTwEnum.RESULT_DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_CRIT)

    RESULT_ELEMENT: str = _(ZhTwEnum.RESULT_ELEMENT)
    RESULT_BONUS_TYPE: str = _(ZhTwEnum.RESULT_BONUS_TYPE)
    RESULT_SKILL_DMG: str = _(ZhTwEnum.RESULT_SKILL_DMG)

    RESULT_ATK: str = _(ZhTwEnum.RESULT_ATK)
    RESULT_ATK_ADDITION: str = _(ZhTwEnum.RESULT_ATK_ADDITION)
    RESULT_ATK_P: str = _(ZhTwEnum.RESULT_ATK_P)
    RESULT_CRIT_RATE: str = _(ZhTwEnum.RESULT_CRIT_RATE)
    RESULT_CRIT_DMG: str = _(ZhTwEnum.RESULT_CRIT_DMG)
    RESULT_BONUS: str = _(ZhTwEnum.RESULT_BONUS)

    MONSTER_LEVEL: str = "[怪物]等級"
    MONSTER_DEF: str = "[怪物]防禦"
    MONSTER_RES: str = "[怪物]抗性"


class CalculatedTemplateRowModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    labels: List[str] = []

    resonator_name: str = ""
    skill_id: str = ""

    resonator_level: Optional[ElementEnum] = None

    resonator_skill_level: str = ""
    resonator_skill_element: Optional[ElementEnum] = None
    resonator_skill_base_attr: Optional[SkillBaseAttrEnum] = None
    resonator_skill_type: Optional[ResonatorSkillTypeEnum] = None
    resonator_skill_type_bonus: Optional[SkillBonusTypeEnum] = None
    resonator_skill_dmg: Optional[Decimal] = None
    resonator_skill_dmg_addition: Optional[Decimal] = None

    echo_element: Optional[ElementEnum] = None
    echo_skill_base_attr: Optional[SkillBaseAttrEnum] = None
    echo_skill_dmg: Optional[Decimal] = None

    damage: Optional[Decimal] = None
    damage_no_crit: Optional[Decimal] = None
    damage_crit: Optional[Decimal] = None

    result_element: Optional[ElementEnum] = None
    result_bonus_type: Optional[SkillBonusTypeEnum] = None
    result_skill_base_attribute: Optional[SkillBaseAttrEnum] = None
    result_skill_dmg: Optional[Decimal] = None
    result_skill_hit: Optional[Decimal] = Decimal("1")

    result_hp: Optional[Decimal] = None
    result_hp_addition: Optional[Decimal] = None
    result_hp_p: Optional[Decimal] = None
    result_atk: Optional[Decimal] = None
    result_atk_addition: Optional[Decimal] = None
    result_atk_p: Optional[Decimal] = None
    result_def: Optional[Decimal] = None
    result_def_addition: Optional[Decimal] = None
    result_def_p: Optional[Decimal] = None

    result_crit_rate: Optional[Decimal] = None
    result_crit_dmg: Optional[Decimal] = None

    result_magnifier: Optional[Decimal] = None
    result_amplifier: Optional[Decimal] = None
    result_bonus: Optional[Decimal] = None
    result_ignore_def: Optional[Decimal] = None
    result_reduce_res: Optional[Decimal] = None

    monster_level: Optional[Decimal] = None
    monster_def: Optional[Decimal] = None
    monster_res: Optional[Decimal] = None

    hits: str = ""
    real_dmg_no_crit: str = ""
    real_dmg_crit: str = ""
    action: str = ""
    time_start: str = ""
    time_end: str = ""
    buffs: List[TemplateBuffTableRowModel] = []

    # @field_validator(
    #     "resonator_skill_element", "echo_element", "result_element", mode="before"
    # )
    # def empty_str_to_none(cls, v):
    #     if v == "":
    #         return None
    #     return v

    # @field_validator("*", mode="after")
    # def none_to_empty_str(cls, v):
    #     if v is None:
    #         return ""
    #     return v
