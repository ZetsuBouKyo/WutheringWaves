from typing import Any, Optional

from ww.model.echoes import EchoesEnum, EchoListEnum
from ww.tables.crud import search
from ww.utils.pd import safe_get_df

ECHOES_PATH = "./cache/v1/custom/echo/echoes.tsv"
ECHOES_HTML_PATH = "./cache/v1/output/echoes.html"
ECHOES_PNG_FNAME = "echoes.png"

ECHOES_LIST_PATH = "./data/v1/echo_list.tsv"


class EchoesTable:
    def __init__(self):
        column_names = [e.value for e in EchoesEnum]
        self.df = safe_get_df(ECHOES_PATH, column_names)

    def search(self, id: str, col: EchoesEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoesEnum.ID.value)


class EchoListTable:
    def __init__(self):
        column_names = [e.value for e in EchoListEnum]
        self.df = safe_get_df(ECHOES_LIST_PATH, column_names)

    def search(self, id: str, col: EchoListEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoListEnum.ID.value)
