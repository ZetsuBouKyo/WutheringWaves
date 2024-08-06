from enum import Enum

from ww.locale import ZhHantEnum, _

TEMPLATE_BONUS = "[額外]"


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


class TemplateRowActionEnum(str, Enum):
    ATTACK: str = "普攻"
    ATTACK_N: str = "普攻xN"
    AIR_ATTACK: str = "空中攻擊"
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


class TemplateRowEnum(str, Enum):
    CALCULATE: str = "計算"
    BONUS_BUFF: str = "增益"
    RESONATOR_NAME: str = "[角色]名稱"

    REAL_DMG_NO_CRIT: str = "[實戰]無暴擊"
    REAL_DMG_CRIT: str = "[實戰]暴擊"

    DAMAGE: str = _(ZhHantEnum.DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhHantEnum.DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhHantEnum.DAMAGE_CRIT)

    ACTION: str = "[實戰]操作"
    SKILL_ID: str = "[實戰]技能代稱"
    SKILL_BONUS_TYPE: str = "[實戰]技能加成種類"

    FINAL_ELEMENT: str = _(ZhHantEnum.FINAL_ELEMENT)
    FINAL_BONUS_TYPE: str = _(ZhHantEnum.FINAL_BONUS_TYPE)
    FINAL_SKILL_DMG: str = _(ZhHantEnum.FINAL_SKILL_DMG)

    FINAL_ATK: str = _(ZhHantEnum.FINAL_ATK)
    FINAL_ATK_ADDITION: str = _(ZhHantEnum.FINAL_ATK_ADDITION)
    FINAL_ATK_P: str = _(ZhHantEnum.FINAL_ATK_P)
    FINAL_CRIT_RATE: str = _(ZhHantEnum.FINAL_CRIT_RATE)
    FINAL_CRIT_DMG: str = _(ZhHantEnum.FINAL_CRIT_DMG)
    FINAL_BONUS: str = _(ZhHantEnum.FINAL_BONUS)

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
