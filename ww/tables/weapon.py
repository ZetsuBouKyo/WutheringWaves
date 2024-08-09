from pathlib import Path
from typing import Any, Optional

from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

WEAPON_HOME_PATH = "./data/v1/武器"
WEAPON_STAT_FNAME = "屬性.tsv"
WEAPON_RANK_FNAME = "諧振.tsv"


def get_weapon_dir_path(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(WEAPON_HOME_PATH) / resonator_name


def get_weapon_stat_fpath(weapon_name: str) -> Optional[Path]:
    if not weapon_name:
        return None
    return Path(WEAPON_HOME_PATH) / weapon_name / WEAPON_STAT_FNAME


def get_weapon_rank_fpath(weapon_name: str) -> Optional[Path]:
    if not weapon_name:
        return None
    return Path(WEAPON_HOME_PATH) / weapon_name / WEAPON_RANK_FNAME


class WeaponStatTable:
    def __init__(self, name):
        _path = get_weapon_stat_fpath(name)
        self.column_names = [e.value for e in WeaponStatEnum]
        if name:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: WeaponStatEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponStatEnum.LEVEL.value)


class WeaponRankTable:
    def __init__(self, name):
        _path = get_weapon_rank_fpath(name)
        self.column_names = [e.value for e in WeaponRankEnum]
        if name:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: WeaponRankEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponRankEnum.LEVEL.value)
