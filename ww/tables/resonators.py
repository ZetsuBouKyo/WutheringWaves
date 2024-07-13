from typing import Any, Optional

from ww.model.resonator import ResonatorEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

RESONATOR_PATH = "./data/自訂/角色"
RESONATOR_HTML_PATH = "./cache/角色.html"
RESONATOR_PNG_FNAME = "角色.png"


class ResonatorsTable:
    def __init__(self):
        self.df = get_df(RESONATOR_PATH)

    def search(self, id: str, col: ResonatorEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorEnum.ID.value)
