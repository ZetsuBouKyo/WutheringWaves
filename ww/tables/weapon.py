from pathlib import Path
from typing import Any, Optional

from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

WEAPON_HOME_PATH = "./data/武器"
WEAPON_STAT_FNAME = "屬性.tsv"
WEAPON_RANK_FNAME = "諧振.tsv"


class WeaponStatTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_HOME_PATH) / name / WEAPON_STAT_FNAME
        self.df = get_df(_stat_path)

    def search(self, id: str, col: WeaponStatEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponStatEnum.LEVEL.value)


class WeaponRankTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_HOME_PATH) / name / WEAPON_RANK_FNAME
        self.df = get_df(_stat_path)

    def search(self, id: str, col: WeaponRankEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponRankEnum.LEVEL.value)
