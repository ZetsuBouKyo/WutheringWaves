from pathlib import Path
from typing import Any, Optional

from ww.model.echo_skill import EchoSkillEnum
from ww.tables.crud import search
from ww.utils.pd import safe_get_df

ECHO_SKILL_PATH = "./data/v1/echo_skills.tsv"


class EchoSkillTable:
    def __init__(self):
        _stat_path = Path(ECHO_SKILL_PATH)
        column_names = [e.value for e in EchoSkillEnum]
        self.df = safe_get_df(_stat_path, column_names)

    def search(self, id: str, col: EchoSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoSkillEnum.SKILL_ID.value)
