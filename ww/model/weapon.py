from enum import Enum

from ww.locale import ZhHantEnum, _


class WeaponPassiveStatEnum(str, Enum):
    ATK_P: str = _(ZhHantEnum.WEAPON_ATK_P_INCREASE)
    ATTRIBUTE_DMG_BONUS: str = _(ZhHantEnum.WEAPON_ATTRIBUTE_DMG_BONUS_INCREASE)
    ENERGY_REGEN: str = _(ZhHantEnum.WEAPON_ENERGY_REGEN_INCREASE)


class WeaponSubStatEnum(str, Enum):
    ATK_P: str = _(ZhHantEnum.ATK_P)
    DEF_P: str = _(ZhHantEnum.DEF_P)
    HP_P: str = _(ZhHantEnum.HP_P)
    CRIT_DMG: str = _(ZhHantEnum.CRIT_DMG)
    CRIT_RATE: str = _(ZhHantEnum.CRIT_RATE)
    ENERGY_REGEN: str = _(ZhHantEnum.ENERGY_REGEN)


class WeaponStatEnum(str, Enum):
    LEVEL: str = _(ZhHantEnum.LEVEL)
    ATK: str = _(ZhHantEnum.ATK)
    ATK_P: str = _(ZhHantEnum.ATK_P)
    DEF_P: str = _(ZhHantEnum.DEF_P)
    HP_P: str = _(ZhHantEnum.HP_P)
    CRIT_DMG: str = _(ZhHantEnum.CRIT_DMG)
    CRIT_RATE: str = _(ZhHantEnum.CRIT_RATE)
    ENERGY_REGEN: str = _(ZhHantEnum.ENERGY_REGEN)


class WeaponRankEnum(str, Enum):
    LEVEL: str = _(ZhHantEnum.LEVEL)
    ATK_P: str = _(ZhHantEnum.WEAPON_ATK_P_INCREASE)
    ATTRIBUTE_DMG_BONUS: str = _(ZhHantEnum.WEAPON_ATTRIBUTE_DMG_BONUS_INCREASE)
    ENERGY_REGEN: str = _(ZhHantEnum.WEAPON_ENERGY_REGEN_INCREASE)
