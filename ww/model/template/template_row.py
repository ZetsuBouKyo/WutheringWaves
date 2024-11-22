from enum import Enum

from ww.locale import ZhTwEnum, _

TEMPLATE_BONUS = "[額外]"  # TODO: remove


class TemplateRowBuffTypeEnum(str, Enum):
    SKILL_DMG_ADDITION: str = _(ZhTwEnum.SKILL_DMG_ADDITION)
    MAGNIFIER: str = _(ZhTwEnum.MAGNIFIER)
    AMPLIFIER: str = _(ZhTwEnum.AMPLIFIER)
    ADDITION: str = _(ZhTwEnum.ADDITION)
    HP_P: str = _(ZhTwEnum.HP_P)
    HP: str = _(ZhTwEnum.HP)
    ATK_P: str = _(ZhTwEnum.ATK_P)
    ATK: str = _(ZhTwEnum.ATK)
    DEF_P: str = _(ZhTwEnum.DEF_P)
    DEF: str = _(ZhTwEnum.DEF)
    CRIT_RATE: str = _(ZhTwEnum.CRIT_RATE)
    CRIT_DMG: str = _(ZhTwEnum.CRIT_DMG)
    IGNORE_DEF: str = _(ZhTwEnum.IGNORE_DEF)
    REDUCE_RES: str = _(ZhTwEnum.REDUCE_RES)


class TemplateRowActionEnum(str, Enum):
    ATTACK: str = "普攻"
    ATTACK_N: str = "普攻xN"
    AIR_ATTACK: str = "空中攻擊"
    HEAVY_ATTACK: str = "重擊"
    AIR_HEAVY_ATTACK: str = "空中重擊"
    RESONANCE_SKILL: str = "共鳴技能"
    RESONANCE_LIBERATION: str = "共鳴解放"
    ECHO: str = "聲骸"
    OUTRO: str = "延奏"
    INTRO: str = "變奏"
    SWITCH: str = "入場"
    SWITCH_AIR: str = "空中入場"
    GRAPPLE: str = "鉤索"
    COORDINATED_ATTACK: str = "協同攻擊"
    DODGE: str = "閃避"
    JUMP: str = "跳"
    NONE: str = "無"


class TemplateColumnEnum(str, Enum):
    LABEL: str = _(ZhTwEnum.LABEL)
    COMMENT: str = _(ZhTwEnum.COMMENT)
    CALCULATE: str = _(ZhTwEnum.CALCULATE)
    BONUS_BUFF: str = _(ZhTwEnum.BUFF)
    RESONATOR_NAME: str = "[角色]名稱"

    REAL_DMG_NO_CRIT: str = "[實戰]無暴擊"
    REAL_DMG_CRIT: str = "[實戰]暴擊"

    DAMAGE_NO_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_CRIT)
    DAMAGE: str = _(ZhTwEnum.RESULT_DAMAGE)

    ACTION: str = "[實戰]操作"
    SKILL_ID: str = "[實戰]技能代稱"
    SKILL_BONUS_TYPE: str = "[實戰]技能加成種類"

    RESULT_BONUS_TYPE: str = _(ZhTwEnum.RESULT_BONUS_TYPE)
    RESULT_ELEMENT: str = _(ZhTwEnum.RESULT_ELEMENT)
    RESULT_SKILL_BASE_ATTRIBUTE: str = _(ZhTwEnum.RESULT_SKILL_BASE_ATTRIBUTE)
    RESULT_SKILL_DMG: str = _(ZhTwEnum.RESULT_SKILL_DMG)

    RESULT_ATK: str = _(ZhTwEnum.RESULT_ATK)
    RESULT_ATK_ADDITION: str = _(ZhTwEnum.RESULT_ATK_ADDITION)
    RESULT_ATK_P: str = _(ZhTwEnum.RESULT_ATK_P)
    RESULT_CRIT_RATE: str = _(ZhTwEnum.RESULT_CRIT_RATE)
    RESULT_CRIT_DMG: str = _(ZhTwEnum.RESULT_CRIT_DMG)
    RESULT_BONUS: str = _(ZhTwEnum.RESULT_BONUS)

    BONUS_SKILL_DMG_ADDITION: str = (
        f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.SKILL_DMG_ADDITION.value}"
    )
    BONUS_MAGNIFIER: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.MAGNIFIER.value}"
    BONUS_AMPLIFIER: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.AMPLIFIER.value}"
    BONUS_ADDITION: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ADDITION.value}"
    BONUS_HP_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.HP_P.value}"
    BONUS_HP: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.HP.value}"
    BONUS_ATK_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ATK_P.value}"
    BONUS_ATK: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.ATK.value}"
    BONUS_DEF_P: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.DEF_P.value}"
    BONUS_DEF: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.DEF.value}"
    BONUS_CRIT_RATE: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.CRIT_RATE.value}"
    BONUS_CRIT_DMG: str = f"{TEMPLATE_BONUS}{TemplateRowBuffTypeEnum.CRIT_DMG.value}"
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
