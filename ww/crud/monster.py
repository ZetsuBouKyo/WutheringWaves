from typing import List

from ww.model.monsters import MonstersEnum
from ww.tables.monster import MonstersTable


def get_monster_ids() -> List[str]:
    table = MonstersTable()
    df = table.df
    names = [name for name in df[MonstersEnum.NAME].to_list() if name]
    return names
