from pathlib import Path
from typing import Any, Optional

from ww.model.resonator import ResonatorStatEnum
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = "./data/v1/角色"
RESONATOR_STAT_FNAME = "屬性.tsv"


def get_resonator_stat_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_STAT_FNAME


class ResonatorStatTable:
    def __init__(self, name):
        _stat_path = get_resonator_stat_fpath(name)
        column_names = [e.value for e in ResonatorStatEnum]
        if _stat_path is not None:
            self.df = safe_get_df(_stat_path, column_names)
        else:
            self.df = get_empty_df(column_names)

    def search(self, id: str, col: ResonatorStatEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorStatEnum.LEVEL.value)
