from enum import Enum

from ww.locale import ZhTwEnum, _


class BuffTargetEnum(str, Enum):
    ALL: str = _(ZhTwEnum.BUFF_TARGET_ALL)
    NEXT: str = _(ZhTwEnum.BUFF_TARGET_NEXT)
    SELF: str = _(ZhTwEnum.BUFF_TARGET_SELF)
    ACTIVE: str = _(ZhTwEnum.BUFF_ACTIVE)


class BuffSourceEnum(str, Enum):
    RESONATOR_INHERENT_SKILL_1: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_INHERENT_SKILL_1)
    RESONATOR_INHERENT_SKILL_2: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_INHERENT_SKILL_2)

    RESONATOR_CHAIN_1: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_1)
    RESONATOR_CHAIN_2: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_2)
    RESONATOR_CHAIN_3: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_3)
    RESONATOR_CHAIN_4: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_4)
    RESONATOR_CHAIN_5: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_5)
    RESONATOR_CHAIN_6: str = _(ZhTwEnum.BUFF_SOURCE_RESONATOR_CHAIN_6)

    NORMAL_ATTACK: str = _(ZhTwEnum.BUFF_SOURCE_NORMAL_ATTACK)
    RESONANCE_SKILL: str = _(ZhTwEnum.BUFF_SOURCE_RESONANCE_SKILL)
    FORTE_CIRCUIT: str = _(ZhTwEnum.BUFF_SOURCE_FORTE_CIRCUIT)
    RESONANCE_LIBERATION: str = _(ZhTwEnum.BUFF_SOURCE_RESONANCE_LIBERATION)
    INTRO_SKILL: str = _(ZhTwEnum.BUFF_SOURCE_INTRO_SKILL)
    OUTRO_SKILL: str = _(ZhTwEnum.BUFF_SOURCE_OUTRO_SKILL)


class ResonatorBuffTsvColumnEnum(str, Enum):
    ID: str = _(ZhTwEnum.BUFF_ID)
    NAME: str = _(ZhTwEnum.BUFF_NAME)
    SOURCE: str = _(ZhTwEnum.BUFF_SOURCE)
    SUFFIX: str = _(ZhTwEnum.BUFF_SUFFIX)
    TYPE: str = _(ZhTwEnum.BUFF_TYPE)
    ELEMENT: str = _(ZhTwEnum.BUFF_ELEMENT)
    SKILL_TYPE: str = _(ZhTwEnum.BUFF_SKILL_TYPE)
    TARGET: str = _(ZhTwEnum.BUFF_TARGET)
    VALUE: str = _(ZhTwEnum.BUFF_VALUE)
    DURATION: str = _(ZhTwEnum.BUFF_DURATION)


class WeaponBuffTsvColumnEnum(str, Enum):
    ID: str = _(ZhTwEnum.BUFF_ID)
    NAME: str = _(ZhTwEnum.BUFF_NAME)
    SUFFIX: str = _(ZhTwEnum.BUFF_SUFFIX)
    RANK: str = _(ZhTwEnum.BUFF_WEAPON_TUNE)
    TYPE: str = _(ZhTwEnum.BUFF_TYPE)
    ELEMENT: str = _(ZhTwEnum.BUFF_ELEMENT)
    SKILL_TYPE: str = _(ZhTwEnum.BUFF_SKILL_TYPE)
    VALUE: str = _(ZhTwEnum.BUFF_VALUE)
    DURATION: str = _(ZhTwEnum.BUFF_DURATION)


class EchoBuffTsvColumnEnum(str, Enum):
    ID: str = _(ZhTwEnum.BUFF_ID)
    NAME: str = _(ZhTwEnum.BUFF_NAME)
    SUFFIX: str = _(ZhTwEnum.BUFF_SUFFIX)
    TYPE: str = _(ZhTwEnum.BUFF_TYPE)
    ELEMENT: str = _(ZhTwEnum.BUFF_ELEMENT)
    SKILL_TYPE: str = _(ZhTwEnum.BUFF_SKILL_TYPE)
    TARGET: str = _(ZhTwEnum.BUFF_TARGET)
    VALUE: str = _(ZhTwEnum.BUFF_VALUE)
    DURATION: str = _(ZhTwEnum.BUFF_DURATION)


class EchoSonataBuffTsvColumnEnum(str, Enum):
    ID: str = _(ZhTwEnum.BUFF_ID)
    NAME: str = _(ZhTwEnum.BUFF_NAME)
    SUFFIX: str = _(ZhTwEnum.BUFF_SUFFIX)
    TYPE: str = _(ZhTwEnum.BUFF_TYPE)
    ELEMENT: str = _(ZhTwEnum.BUFF_ELEMENT)
    SKILL_TYPE: str = _(ZhTwEnum.BUFF_SKILL_TYPE)
    TARGET: str = _(ZhTwEnum.BUFF_TARGET)
    VALUE: str = _(ZhTwEnum.BUFF_VALUE)
    DURATION: str = _(ZhTwEnum.BUFF_DURATION)


class SkillBonusTypeEnum(str, Enum):
    BASIC: str = _(ZhTwEnum.BASIC)
    HEAVY: str = _(ZhTwEnum.HEAVY)
    SKILL: str = _(ZhTwEnum.RESONANCE_SKILL)
    LIBERATION: str = _(ZhTwEnum.RESONANCE_LIBERATION)
    INTRO: str = _(ZhTwEnum.INTRO)
    OUTRO: str = _(ZhTwEnum.OUTRO)
    ECHO: str = _(ZhTwEnum.ECHO)
    COORDINATED_ATTACK: str = _(ZhTwEnum.COORDINATED_ATTACK)
    NONE: str = _(ZhTwEnum.NONE)
