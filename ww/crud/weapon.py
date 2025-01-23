import json
from pathlib import Path
from typing import List, Optional

from ww.model.weapon import WeaponInfo
from ww.tables.weapon import WEAPON_HOME_PATH

WEAPONS_INFO_FPATH = "./data/v1/zh_tw/weapons_info.json"


def get_weapon_names() -> List[str]:
    home_path = Path(WEAPON_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_weapon_ranks() -> List[str]:
    ranks = [str(i) for i in range(1, 6)]
    return ranks


def get_weapon_levels() -> List[str]:
    levels = [str(i) for i in range(10, 100, 10)] + [
        "1",
        "20+",
        "40+",
        "60+",
        "70+",
        "80+",
    ]
    levels.sort()
    return levels


class CrudWeapons:

    def __init__(self, weapons_info_fpath: str = WEAPONS_INFO_FPATH):
        self._weapons_info_fpath = Path(weapons_info_fpath)

        self.load()

    def load(self):
        with self._weapons_info_fpath.open(mode="r", encoding="utf-8") as fp:
            weapons = json.load(fp)

        self._no_to_weapon = {}
        self._name_to_weapon = {}

        for weapon in weapons:
            w = WeaponInfo(**weapon)
            self._no_to_weapon[w.no] = w
            self._name_to_weapon[w.name] = w

    def get_weapon_by_no(self, no: str) -> Optional[WeaponInfo]:
        return self._no_to_weapon.get(no, None)

    def get_weapon_by_name(self, name: str) -> Optional[WeaponInfo]:
        return self._name_to_weapon.get(name, None)


crud_weapons = CrudWeapons()
