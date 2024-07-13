from pathlib import Path
from typing import Any, Optional

from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

WEAPON_STAT_HOME_PATH = "./data/武器"
WEAPON_STAT = "屬性"
WEAPON_RANK = "諧振"


class WeaponStatTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_STAT_HOME_PATH) / name / WEAPON_STAT
        self.df = get_df(_stat_path)

    def search(self, id: str, col: WeaponStatEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponStatEnum.LEVEL.value)


class WeaponRankTable:
    def __init__(self, name):
        _stat_path = Path(WEAPON_STAT_HOME_PATH) / name / WEAPON_RANK
        self.df = get_df(_stat_path)

    def search(self, id: str, col: WeaponRankEnum) -> Optional[Any]:
        return search(self.df, id, col, WeaponRankEnum.LEVEL.value)
