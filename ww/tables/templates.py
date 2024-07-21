from pathlib import Path
from typing import Any, Optional

from ww.model.templates import TemplatesEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

TEMPLATES_HOME_PATH = "./data/角色"


class TemplatesTable:
    def __init__(self, name):
        _stat_path = Path(TEMPLATES_HOME_PATH) / name
        self.df = get_df(_stat_path)

    def search(self, id: str, col: TemplatesEnum) -> Optional[Any]:
        return search(self.df, id, col, TemplatesEnum.ID.value)
