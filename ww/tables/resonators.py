from typing import Any, List, Optional

from ww.model.resonator import CalculatedResonatorColumnEnum, ResonatorColumnEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import safe_get_df

RESONATORS_PATH = "./cache/v1/zh_tw/custom/resonator/resonators.tsv"

CALCULATED_RESONATOR_PATH = "./cache/v1/zh_tw/output/[calculated]resonators.tsv"


class ResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in ResonatorColumnEnum]
        self.df = safe_get_df(RESONATORS_PATH, self.column_names)

    def search(self, id: str, col: ResonatorColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, ResonatorColumnEnum.ID.value)


class CalculatedResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in CalculatedResonatorColumnEnum]
        self.df = safe_get_df(CALCULATED_RESONATOR_PATH, self.column_names)

    def search(self, id: str, col: CalculatedResonatorColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, CalculatedResonatorColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, CalculatedResonatorColumnEnum.ID.value)
