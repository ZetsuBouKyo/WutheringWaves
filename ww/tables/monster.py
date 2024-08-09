from pathlib import Path
from typing import Any, Optional

from ww.model.monsters import MonstersEnum
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

MONSTERS_PATH = "./data/v1/monster.tsv"


def get_monsters_fpath() -> Path:
    return Path(MONSTERS_PATH)


class MonstersTable:
    def __init__(self):
        _path = get_monsters_fpath()
        self.column_names = [e.value for e in MonstersEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: MonstersEnum) -> Optional[Any]:
        return search(self.df, id, col, MonstersEnum.NAME.value)
