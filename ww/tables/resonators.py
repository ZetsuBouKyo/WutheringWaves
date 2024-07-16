from typing import Any, Optional

from ww.model.resonators import ResonatorsEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

RESONATORS_PATH = "./data/自訂/角色.tsv"

CALCULATED_RESONATOR_PATH = "./cache/[計算用]角色.tsv"


class ResonatorsTable:
    def __init__(self):
        self.df = get_df(RESONATORS_PATH)

    def search(self, id: str, col: ResonatorsEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorsEnum.ID.value)


class CalculatedResonatorsTable:
    def __init__(self):
        self.df = get_df(CALCULATED_RESONATOR_PATH)

    def search(self, id: str, col: ResonatorsEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorsEnum.ID.value)
