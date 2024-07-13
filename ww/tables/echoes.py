from typing import Any, Optional

from ww.model.echo import EchoesEnum
from ww.utils.pd import get_df

ECHOES_PATH = "./data/自訂/聲骸"
ECHOES_HTML_PATH = "./cache/聲骸.html"
ECHOES_PNG_FNAME = "聲骸.png"


class EchoesTable:
    def __init__(self):
        self.df = get_df(ECHOES_PATH)

    def search(self, id: str, col: EchoesEnum) -> Optional[Any]:
        df = self.df

        rows = df.loc[df[EchoesEnum.ID.value] == id]
        assert len(rows.values) <= 1, f"ID: {id} must be unique"
        if len(rows.values) == 0:
            print(f"ID: {id} not found")
            return None

        cells = rows[col].values
        assert len(cells) <= 1, f"Column name: {col} must be unique"
        if len(cells) == 0:
            print(f"ID: {id} with column: {col} not found")
            return None

        return cells[0]
