from typing import Any, Optional

from ww.model.echoes import EchoesEnum, EchoListEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

ECHOES_PATH = "./cache/v1/自訂/聲骸.tsv"
ECHOES_HTML_PATH = "./cache/v1/聲骸.html"
ECHOES_PNG_FNAME = "聲骸.png"

ECHOES_LIST_PATH = "./data/v1/聲骸列表.tsv"


class EchoesTable:
    def __init__(self):
        self.df = get_df(ECHOES_PATH)

    def search(self, id: str, col: EchoesEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoesEnum.ID.value)


class EchoListTable:
    def __init__(self):
        self.df = get_df(ECHOES_LIST_PATH)

    def search(self, id: str, col: EchoListEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoListEnum.ID.value)
