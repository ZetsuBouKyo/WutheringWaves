from enum import Enum

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
