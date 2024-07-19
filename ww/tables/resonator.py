from pathlib import Path
from typing import Any, Optional

from ww.model.resonator import ResonatorEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

RESONATOR_HOME_PATH = "./data/角色"
RESONATOR_STAT_FNAME = "屬性.tsv"


class ResonatorStatTable:
    def __init__(self, name):
        _stat_path = Path(RESONATOR_HOME_PATH) / name / RESONATOR_STAT_FNAME
        self.df = get_df(_stat_path)

    def search(self, id: str, col: ResonatorEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorEnum.LEVEL.value)
