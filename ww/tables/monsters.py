from typing import Any, Optional

from ww.model.monsters import MonstersEnum
from ww.tables.crud import search
from ww.utils.pd import safe_get_df

MONSTERS_PATH = "./data/v1/monster.tsv"


class MonstersTable:
    def __init__(self):
        column_names = [e.value for e in MonstersEnum]
        self.df = safe_get_df(MONSTERS_PATH, column_names)

    def search(self, id: str, col: MonstersEnum) -> Optional[Any]:
        return search(self.df, id, col, MonstersEnum.NAME.value)
