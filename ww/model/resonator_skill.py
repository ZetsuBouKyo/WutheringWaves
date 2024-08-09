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
    BASIC: str = _(ZhHantEnum.BASIC)
    HEAVY: str = _(ZhHantEnum.HEAVY)
    SKILL: str = _(ZhHantEnum.SKILL)
    LIBERATION: str = _(ZhHantEnum.LIBERATION)
    INTRO: str = _(ZhHantEnum.INTRO)
    OUTRO: str = _(ZhHantEnum.OUTRO)
    ECHO: str = _(ZhHantEnum.ECHO)
    NONE: str = _(ZhHantEnum.NONE)


class ResonatorSkillEnum(str, Enum):
    TYPE_BONUS: str = _(ZhHantEnum.RESONATOR_SKILL_TYPE_BONUS)
    PRIMARY_KEY: str = _(ZhHantEnum.RESONATOR_SKILL_PRIMARY_KEY)
    TYPE_ZH_HANT: str = _(ZhHantEnum.RESONATOR_SKILL_TYPE_ZH_HANT)

    ENTRY: str = _(ZhHantEnum.RESONATOR_SKILL_ENTRY)
    ELEMENT: str = _(ZhHantEnum.RESONATOR_SKILL_ELEMENT)
    BASE_TYPE: str = _(ZhHantEnum.RESONATOR_SKILL_BASE_TYPE)
    BASE_ATTR: str = _(ZhHantEnum.RESONATOR_SKILL_BASE_ATTR)

    LV1: str = _(ZhHantEnum.RESONATOR_SKILL_LV1)
    LV2: str = _(ZhHantEnum.RESONATOR_SKILL_LV2)
    LV3: str = _(ZhHantEnum.RESONATOR_SKILL_LV3)
    LV4: str = _(ZhHantEnum.RESONATOR_SKILL_LV4)
    LV5: str = _(ZhHantEnum.RESONATOR_SKILL_LV5)
    LV6: str = _(ZhHantEnum.RESONATOR_SKILL_LV6)
    LV7: str = _(ZhHantEnum.RESONATOR_SKILL_LV7)
    LV8: str = _(ZhHantEnum.RESONATOR_SKILL_LV8)
    LV9: str = _(ZhHantEnum.RESONATOR_SKILL_LV9)
    LV10: str = _(ZhHantEnum.RESONATOR_SKILL_LV10)

    RESONANCE_LIBERATION_ENERGY: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY
    )
    RESONATING_SPIN_CONCERTO_ENERGY: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY
    )
    HARDNESS: str = _(ZhHantEnum.RESONATOR_SKILL_HARDNESS)
    TOUGHNESS: str = _(ZhHantEnum.RESONATOR_SKILL_TOUGHNESS)
    TYPE_EN: str = _(ZhHantEnum.RESONATOR_SKILL_TYPE_EN)
    HIT: str = _(ZhHantEnum.RESONATOR_SKILL_HIT)
    STA_REGEN: str = _(ZhHantEnum.RESONATOR_SKILL_STA_REGEN)
    STA: str = _(ZhHantEnum.RESONATOR_SKILL_STA)
    SPECIAL_ENERGY_REGEN: str = _(ZhHantEnum.RESONATOR_SKILL_SPECIAL_ENERGY_REGEN)
    SPECIAL_ENERGY: str = _(ZhHantEnum.RESONATOR_SKILL_SPECIAL_ENERGY)
    RESONATING_SPIN_CONCERTO_ENERGY_REGEN: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY_REGEN
    )
    RESONATING_SPIN_CONCERTO_ENERGY_CONSUME: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY_CONSUME
    )
    RESONANCE_LIBERATION_ENERGY_REGEN: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY_REGEN
    )
    RESONANCE_LIBERATION_ENERGY_CONSUME: str = _(
        ZhHantEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY_CONSUME
    )
    COOLDOWN: str = _(ZhHantEnum.RESONATOR_SKILL_COOLDOWN)
    DURATION: str = _(ZhHantEnum.RESONATOR_SKILL_DURATION)
    HEALING: str = _(ZhHantEnum.RESONATOR_SKILL_HEALING)
    IGNORE_DEF: str = _(ZhHantEnum.RESONATOR_SKILL_IGNORE_DEF)
    REDUCE_RES: str = _(ZhHantEnum.RESONATOR_SKILL_REDUCE_RES)
