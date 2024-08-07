from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ww.locale import ZhHantEnum, _
from ww.model.element import ElementEnum
from ww.model.resonator_skill import (
    ResonatorSkillBaseAttrEnum,
    ResonatorSkillBonusTypeEnum,
    ResonatorSkillTypeEnum,
)


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

    DAMAGE: str = _(ZhHantEnum.DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhHantEnum.DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhHantEnum.DAMAGE_CRIT)

    FINAL_ELEMENT: str = _(ZhHantEnum.FINAL_ELEMENT)
    FINAL_BONUS_TYPE: str = _(ZhHantEnum.FINAL_BONUS_TYPE)
    FINAL_SKILL_DMG: str = _(ZhHantEnum.FINAL_SKILL_DMG)

    FINAL_ATK: str = _(ZhHantEnum.FINAL_ATK)
    FINAL_ATK_ADDITION: str = _(ZhHantEnum.FINAL_ATK_ADDITION)
    FINAL_ATK_P: str = _(ZhHantEnum.FINAL_ATK_P)
    FINAL_CRIT_RATE: str = _(ZhHantEnum.FINAL_CRIT_RATE)
    FINAL_CRIT_DMG: str = _(ZhHantEnum.FINAL_CRIT_DMG)
    FINAL_BONUS: str = _(ZhHantEnum.FINAL_BONUS)

    MONSTER_LEVEL: str = "[怪物]等級"
    MONSTER_DEF: str = "[怪物]防禦"
    MONSTER_RES: str = "[怪物]抗性"


class CalculatedTemplateRowModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    resonator_name: str = ""
    skill_id: str = ""

    resonator_skill_level: str = ""
    resonator_skill_element: Optional[ElementEnum] = None
    resonator_skill_base_attr: Optional[ResonatorSkillBaseAttrEnum] = None
    resonator_skill_type: Optional[ResonatorSkillTypeEnum] = None
    resonator_skill_type_bonus: Optional[ResonatorSkillBonusTypeEnum] = None
    resonator_skill_dmg: Optional[Decimal] = None

    echo_element: Optional[ElementEnum] = None
    echo_skill_dmg: Optional[Decimal] = None

    damage: Optional[Decimal] = None
    damage_no_crit: Optional[Decimal] = None
    damage_crit: Optional[Decimal] = None

    final_element: Optional[ElementEnum] = None
    final_bonus_type: Optional[ResonatorSkillBonusTypeEnum] = None
    final_skill_dmg: Optional[Decimal] = None

    final_atk: Optional[Decimal] = None
    final_atk_addition: Optional[Decimal] = None
    final_atk_p: Optional[Decimal] = None
    final_crit_rate: Optional[Decimal] = None
    final_crit_dmg: Optional[Decimal] = None
    final_bonus: Optional[Decimal] = None

    monster_level: Optional[Decimal] = None
    monster_def: Optional[Decimal] = None
    monster_res: Optional[Decimal] = None

    # @field_validator(
    #     "resonator_skill_element", "echo_element", "final_element", mode="before"
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
