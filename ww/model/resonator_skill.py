from enum import Enum

from pydantic import BaseModel

from ww.locale import ZhTwEnum, _


class SkillBaseAttrEnum(str, Enum):
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)


class ResonatorSkillTypeEnum(str, Enum):
    NORMAL_ATTACK: str = _(ZhTwEnum.NORMAL_ATTACK)
    RESONANCE_SKILL: str = _(ZhTwEnum.RESONANCE_SKILL)
    FORTE_CIRCUIT: str = _(ZhTwEnum.FORTE_CIRCUIT)
    RESONANCE_LIBERATION: str = _(ZhTwEnum.RESONANCE_LIBERATION)
    INTRO_SKILL: str = _(ZhTwEnum.INTRO_SKILL)
    OUTRO_SKILL: str = _(ZhTwEnum.OUTRO_SKILL)


class ResonatorSkillBonusTypeEnum(str, Enum):
    BASIC: str = _(ZhTwEnum.BASIC)
    HEAVY: str = _(ZhTwEnum.HEAVY)
    RESONANCE_SKILL: str = _(ZhTwEnum.RESONANCE_SKILL)
    RESONANCE_LIBERATION: str = _(ZhTwEnum.RESONANCE_LIBERATION)
    NONE: str = _(ZhTwEnum.NONE)


class ResonatorSkillTsvColumnEnum(str, Enum):
    SKILL_BONUS_TYPE: str = _(ZhTwEnum.RESONATOR_SKILL_BONUS_TYPE)
    PRIMARY_KEY: str = _(ZhTwEnum.RESONATOR_SKILL_PRIMARY_KEY)
    TYPE_ZH_TW: str = _(ZhTwEnum.RESONATOR_SKILL_TYPE_ZH_TW)

    ENTRY: str = _(ZhTwEnum.RESONATOR_SKILL_ENTRY)
    ELEMENT: str = _(ZhTwEnum.RESONATOR_SKILL_ELEMENT)
    BASE_TYPE: str = _(ZhTwEnum.RESONATOR_SKILL_BASE_TYPE)
    BASE_ATTR: str = _(ZhTwEnum.RESONATOR_SKILL_BASE_ATTR)

    LV1: str = _(ZhTwEnum.RESONATOR_SKILL_LV1)
    LV2: str = _(ZhTwEnum.RESONATOR_SKILL_LV2)
    LV3: str = _(ZhTwEnum.RESONATOR_SKILL_LV3)
    LV4: str = _(ZhTwEnum.RESONATOR_SKILL_LV4)
    LV5: str = _(ZhTwEnum.RESONATOR_SKILL_LV5)
    LV6: str = _(ZhTwEnum.RESONATOR_SKILL_LV6)
    LV7: str = _(ZhTwEnum.RESONATOR_SKILL_LV7)
    LV8: str = _(ZhTwEnum.RESONATOR_SKILL_LV8)
    LV9: str = _(ZhTwEnum.RESONATOR_SKILL_LV9)
    LV10: str = _(ZhTwEnum.RESONATOR_SKILL_LV10)

    RESONANCE_LIBERATION_ENERGY: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY
    )
    RESONATING_SPIN_CONCERTO_ENERGY: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY
    )
    HARDNESS: str = _(ZhTwEnum.RESONATOR_SKILL_HARDNESS)
    TOUGHNESS: str = _(ZhTwEnum.RESONATOR_SKILL_TOUGHNESS)
    COORDINATED: str = _(ZhTwEnum.RESONATOR_SKILL_COORDINATED)
    TYPE_EN: str = _(ZhTwEnum.RESONATOR_SKILL_TYPE_EN)
    HIT: str = _(ZhTwEnum.RESONATOR_SKILL_HIT)
    STA_REGEN: str = _(ZhTwEnum.RESONATOR_SKILL_STA_REGEN)
    STA: str = _(ZhTwEnum.RESONATOR_SKILL_STA)
    SPECIAL_ENERGY_REGEN: str = _(ZhTwEnum.RESONATOR_SKILL_SPECIAL_ENERGY_REGEN)
    SPECIAL_ENERGY: str = _(ZhTwEnum.RESONATOR_SKILL_SPECIAL_ENERGY)
    RESONATING_SPIN_CONCERTO_ENERGY_REGEN: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY_REGEN
    )
    RESONATING_SPIN_CONCERTO_ENERGY_CONSUME: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONATING_SPIN_CONCERTO_ENERGY_CONSUME
    )
    RESONANCE_LIBERATION_ENERGY_REGEN: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY_REGEN
    )
    RESONANCE_LIBERATION_ENERGY_CONSUME: str = _(
        ZhTwEnum.RESONATOR_SKILL_RESONANCE_LIBERATION_ENERGY_CONSUME
    )
    COOLDOWN: str = _(ZhTwEnum.RESONATOR_SKILL_COOLDOWN)
    DURATION: str = _(ZhTwEnum.RESONATOR_SKILL_DURATION)
    HEALING: str = _(ZhTwEnum.RESONATOR_SKILL_HEALING)
    IGNORE_DEF: str = _(ZhTwEnum.RESONATOR_SKILL_IGNORE_DEF)
    REDUCE_RES: str = _(ZhTwEnum.RESONATOR_SKILL_REDUCE_RES)


class ResonatorSkillModel(BaseModel):
    skill_type: str = ""
    skill_name: str = ""
    skill_bonus_type: str = ""
    base_attribute: str = ""
    resonance_energy: str = ""
    concerto_energy: str = ""
    lv_1: str = ""
    lv_2: str = ""
    lv_3: str = ""
    lv_4: str = ""
    lv_5: str = ""
    lv_6: str = ""
    lv_7: str = ""
    lv_8: str = ""
    lv_9: str = ""
    lv_10: str = ""
