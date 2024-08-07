from enum import Enum

from pydantic import BaseModel, ConfigDict

from ww.locale import ZhHantEnum, _


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
    resonator_skill_element: str = ""
    resonator_skill_base_attr: str = ""
    resonator_skill_type: str = ""
    resonator_skill_type_bonus: str = ""
    resonator_skill_dmg: str = ""

    echo_element: str = ""
    echo_skill_dmg: str = ""

    damage: str = ""
    damage_no_crit: str = ""
    damage_crit: str = ""

    final_element: str = ""
    final_bonus_type: str = ""
    final_skill_dmg: str = ""

    final_atk: str = ""
    final_atk_addition: str = ""
    final_atk_p: str = ""
    final_crit_rate: str = ""
    final_crit_dmg: str = ""
    final_bonus: str = ""

    monster_level: str = ""
    monster_def: str = ""
    monster_res: str = ""
