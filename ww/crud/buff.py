from typing import Dict, List

from ww.model.buff import BuffSourceEnum, BuffTargetEnum, SkillBonusTypeEnum
from ww.tables.buff import (
    EchoBuffTable,
    EchoSonataBuffTable,
    ResonatorBuffTable,
    WeaponBuffTable,
)


def get_buff_targets() -> List[str]:
    return [e.value for e in BuffTargetEnum]


def get_buff_sources() -> List[str]:
    return [e.value for e in BuffSourceEnum]


def get_resonator_buffs(name: str) -> List[Dict[str, str]]:
    table = ResonatorBuffTable()
    return table.get_rows(name)


def get_weapon_buffs(name: str) -> List[Dict[str, str]]:
    table = WeaponBuffTable()
    return table.get_rows(name)


def get_echo_buffs(name: str) -> List[Dict[str, str]]:
    table = EchoBuffTable()
    return table.get_rows(name)


def get_echo_sonata_buffs(name: str) -> List[Dict[str, str]]:
    table = EchoSonataBuffTable()
    return table.get_rows(name)


def get_skill_bonus_types() -> List[str]:
    return [e.value for e in SkillBonusTypeEnum]
