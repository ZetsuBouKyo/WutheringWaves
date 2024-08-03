from typing import Dict, List

from ww.tables.buff import (
    EchoBuffTable,
    EchoSonataBuffTable,
    ResonatorBuffTable,
    WeaponBuffTable,
)


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
