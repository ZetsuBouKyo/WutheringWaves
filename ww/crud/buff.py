import json
from typing import Dict, List

from ww.locale import ZhTwEnum, _
from ww.model.buff import BuffSourceEnum, BuffTargetEnum, SkillBonusTypeEnum
from ww.tables.buff import (
    EchoBuffTable,
    EchoSonataBuffTable,
    ResonatorBuffTable,
    WeaponBuffTable,
)
from ww.tables.echo import (
    get_echo_skill_descriptions_fpath,
    get_echo_sonata_descriptions_fpath,
)
from ww.tables.resonator import get_resonator_skill_information_fpath
from ww.tables.weapon import get_weapon_information_fpath


def get_buff_targets() -> List[str]:
    return [e.value for e in BuffTargetEnum]


def get_buff_sources() -> List[str]:
    return [e.value for e in BuffSourceEnum]


def get_resonator_buffs(name: str) -> List[Dict[str, str]]:
    table = ResonatorBuffTable()
    return table.get_rows(name)


def get_resonator_buff_description(name: str, source: str) -> str:
    fpath = get_resonator_skill_information_fpath(name)
    if not fpath.exists():
        return ""

    with fpath.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)

    skill = data.get(source, {})
    name = skill.get(_(ZhTwEnum.NAME), "")
    description = skill.get(_(ZhTwEnum.DESCRIPTION), "")
    return f"{name}\n\n{description}"


def add_resonator_buff_descriptions(data: List[Dict[str, str]]):
    for i in range(len(data)):
        name = data[i].get(_(ZhTwEnum.BUFF_NAME), None)
        source = data[i].get(_(ZhTwEnum.BUFF_SOURCE), None)
        if name is None or source is None:
            description = ""
        else:
            description = get_resonator_buff_description(name, source)
        data[i][_(ZhTwEnum.DESCRIPTION)] = description


def get_weapon_buffs(name: str) -> List[Dict[str, str]]:
    table = WeaponBuffTable()
    return table.get_rows(name)


def get_weapon_buff_description(name: str) -> str:
    fpath = get_weapon_information_fpath(name)
    if not fpath.exists():
        return ""

    with fpath.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
    name = data.get(_(ZhTwEnum.NAME), "")
    description = data.get(_(ZhTwEnum.DESCRIPTION), "")
    return f"{name}\n\n{description}"


def add_weapon_buff_descriptions(data: List[Dict[str, str]]):
    for i in range(len(data)):
        name = data[i].get(_(ZhTwEnum.BUFF_NAME), None)
        if name is None:
            description = ""
        else:
            description = get_weapon_buff_description(name)
        data[i][_(ZhTwEnum.DESCRIPTION)] = description


def get_echo_buffs(name: str) -> List[Dict[str, str]]:
    table = EchoBuffTable()
    return table.get_rows(name)


def get_echo_buff_description(name: str) -> str:
    fpath = get_echo_skill_descriptions_fpath()
    if not fpath.exists():
        return ""

    with fpath.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
    description = data.get(name, "")
    return description


def add_echo_buff_descriptions(data: List[Dict[str, str]]):
    for i in range(len(data)):
        name = data[i].get(_(ZhTwEnum.BUFF_NAME), None)
        if name is None:
            description = ""
        else:
            description = get_echo_buff_description(name)
        data[i][_(ZhTwEnum.DESCRIPTION)] = description


def get_echo_sonata_buffs(name: str) -> List[Dict[str, str]]:
    table = EchoSonataBuffTable()
    return table.get_rows(name)


def get_echo_sonata_buff_description(name: str, piece: str = "5") -> str:
    fpath = get_echo_sonata_descriptions_fpath()
    if not fpath.exists():
        return ""

    with fpath.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
    sonata = data.get(name, {})
    description = sonata.get(piece, "")
    return description


def add_echo_sonata_buff_descriptions(data: List[Dict[str, str]]):
    for i in range(len(data)):
        name = data[i].get(_(ZhTwEnum.BUFF_NAME), None)
        if name is None:
            description = ""
        else:
            description = get_echo_sonata_buff_description(name)
        data[i][_(ZhTwEnum.DESCRIPTION)] = description


def get_skill_bonus_types() -> List[str]:
    return [e.value for e in SkillBonusTypeEnum]
