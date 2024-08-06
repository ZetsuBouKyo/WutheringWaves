from pathlib import Path
from typing import Any, Optional

from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

WEAPON_HOME_PATH = "./data/v1/武器"
WEAPON_STAT_FNAME = "屬性.tsv"
WEAPON_RANK_FNAME = "諧振.tsv"


class WeaponStatTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_HOME_PATH) / name / WEAPON_STAT_FNAME
        column_names = [e.value for e in WeaponStatEnum]
        if name:
            self.df = safe_get_df(_stat_path, column_names)
        else:
            self.df = get_empty_df(column_names)

    def search(self, id: str, col: WeaponStatEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponStatEnum.LEVEL.value)


class WeaponRankTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_HOME_PATH) / name / WEAPON_RANK_FNAME
        column_names = [e.value for e in WeaponRankEnum]
        if name:
            self.df = safe_get_df(_stat_path, column_names)
        else:
            self.df = get_empty_df(column_names)

    def search(self, id: str, col: WeaponRankEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponRankEnum.LEVEL.value)
