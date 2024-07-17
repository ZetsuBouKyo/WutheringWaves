from enum import Enum


class ResonatorSkillBaseAttrEnum(str, Enum):
    HP: str = "生命"
    ATK: str = "攻擊"
    DEF: str = "防禦"


class ResonatorSkillTypeEnum(str, Enum):
    NORMAL_ATTACK: str = "常態攻擊"
    RESONANCE_SKILL: str = "共鳴技能"
    RESONANCE_LIBERATION: str = "共鳴解放"
    INTRO_SKILL: str = "變奏技能"
    OUTRO_SKILL: str = "延奏技能"
    FORTE_CIRCUIT: str = "共鳴回路"


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
