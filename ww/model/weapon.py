from enum import Enum

from pydantic import BaseModel

from ww.locale import ZhTwEnum, _


class WeaponPassiveStatEnum(str, Enum):
    ATK_P: str = _(ZhTwEnum.WEAPON_ATK_P_INCREASE)
    HP_P: str = _(ZhTwEnum.WEAPON_HP_P_INCREASE)
    ATTRIBUTE_DMG_BONUS: str = _(ZhTwEnum.WEAPON_ATTRIBUTE_DMG_BONUS_INCREASE)
    ENERGY_REGEN: str = _(ZhTwEnum.WEAPON_ENERGY_REGEN_INCREASE)


class WeaponSubStatEnum(str, Enum):
    ATK_P: str = _(ZhTwEnum.ATK_P)
    DEF_P: str = _(ZhTwEnum.DEF_P)
    HP_P: str = _(ZhTwEnum.HP_P)
    CRIT_DMG: str = _(ZhTwEnum.CRIT_DMG)
    CRIT_RATE: str = _(ZhTwEnum.CRIT_RATE)
    ENERGY_REGEN: str = _(ZhTwEnum.ENERGY_REGEN)


class WeaponStatEnum(str, Enum):
    LEVEL: str = _(ZhTwEnum.LEVEL)
    ATK: str = _(ZhTwEnum.ATK)
    ATK_P: str = _(ZhTwEnum.ATK_P)
    DEF_P: str = _(ZhTwEnum.DEF_P)
    HP_P: str = _(ZhTwEnum.HP_P)
    CRIT_DMG: str = _(ZhTwEnum.CRIT_DMG)
    CRIT_RATE: str = _(ZhTwEnum.CRIT_RATE)
    ENERGY_REGEN: str = _(ZhTwEnum.ENERGY_REGEN)


class WeaponRankEnum(str, Enum):
    LEVEL: str = _(ZhTwEnum.LEVEL)
    ATK_P: str = _(ZhTwEnum.WEAPON_ATK_P_INCREASE)
    HP_P: str = _(ZhTwEnum.WEAPON_HP_P_INCREASE)
    CRIT_RATE: str = _(ZhTwEnum.WEAPON_CRIT_RATE_INCREASE)
    ATTRIBUTE_DMG_BONUS: str = _(ZhTwEnum.WEAPON_ATTRIBUTE_DMG_BONUS_INCREASE)
    ENERGY_REGEN: str = _(ZhTwEnum.WEAPON_ENERGY_REGEN_INCREASE)


class WeaponInfo(BaseModel):
    no: str = ""
    name: str = ""
    star: str = ""
    skill_name: str = ""
    skill_description: str = ""
