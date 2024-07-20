from typing import Any, Optional

from ww.model.echo import EchoesEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

ECHOES_PATH = "./cache/自訂/聲骸.tsv"
ECHOES_HTML_PATH = "./cache/聲骸.html"
ECHOES_PNG_FNAME = "聲骸.png"


class EchoesTable:
    def __init__(self):
        self.df = get_df(ECHOES_PATH)

    def search(self, id: str, col: EchoesEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoesEnum.ID.value)
