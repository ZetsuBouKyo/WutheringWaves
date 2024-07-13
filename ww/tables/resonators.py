from typing import Any, Optional

from ww.model.resonators import ResonatorsEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

RESONATORS_PATH = "./data/自訂/角色"
RESONATORS_HTML_PATH = "./cache/角色.html"
RESONATORS_PNG_FNAME = "角色.png"


class ResonatorsTable:
    def __init__(self):
        self.df = get_df(RESONATORS_PATH)

    def search(self, id: str, col: ResonatorsEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorsEnum.ID.value)
