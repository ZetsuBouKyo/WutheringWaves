from typing import Any, Optional

from ww.model.monsters import MonstersEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

MONSTERS_PATH = "./data/自訂/怪物"


class MonstersTable:
    def __init__(self):
        self.df = get_df(MONSTERS_PATH)

    def search(self, id: str, col: MonstersEnum) -> Optional[Any]:
        return search(self.df, id, col, MonstersEnum.NAME.value)
