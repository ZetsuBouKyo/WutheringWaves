from enum import Enum

from ww.locale import ZhHantEnum, _


class ResonatorSkillBaseAttrEnum(str, Enum):
    HP: str = _(ZhHantEnum.HP)
    ATK: str = _(ZhHantEnum.ATK)
    DEF: str = _(ZhHantEnum.DEF)


class ResonatorSkillTypeEnum(str, Enum):
    NORMAL_ATTACK: str = _(ZhHantEnum.NORMAL_ATTACK)
    RESONANCE_SKILL: str = _(ZhHantEnum.RESONANCE_SKILL)
    RESONANCE_LIBERATION: str = _(ZhHantEnum.RESONANCE_LIBERATION)
    INTRO_SKILL: str = _(ZhHantEnum.INTRO_SKILL)
    OUTRO_SKILL: str = _(ZhHantEnum.OUTRO_SKILL)
    FORTE_CIRCUIT: str = _(ZhHantEnum.FORTE_CIRCUIT)


class ResonatorSkillBonusTypeEnum(str, Enum):
    BASIC: str = "普攻"
    HEAVY: str = "重擊"
    SKILL: str = "共鳴技能"
    LIBERATION: str = "共鳴解放"
    INTRO: str = "變奏"
    OUTRO: str = "延奏"
    ECHO: str = "聲骸"
    NONE: str = "無"


class ResonatorSkillEnum(str, Enum):
    SKILL_ID: str = "代稱"
    SKILL_ELEMENT: str = "屬性"
    SKILL_BASE_ATTR: str = "Base Attribute"
    SKILL_TYPE: str = "種類"
    SKILL_TYPE_BONUS: str = "種類加成"
    SKILL_LV1: str = "LV1"
    SKILL_LV2: str = "LV2"
    SKILL_LV3: str = "LV3"
    SKILL_LV4: str = "LV4"
    SKILL_LV5: str = "LV5"
    SKILL_LV6: str = "LV6"
    SKILL_LV7: str = "LV7"
    SKILL_LV8: str = "LV8"
    SKILL_LV9: str = "LV9"
    SKILL_LV10: str = "LV10"
