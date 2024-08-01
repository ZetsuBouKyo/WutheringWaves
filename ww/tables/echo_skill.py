from pathlib import Path
from typing import Any, Optional

from ww.model.echo_skill import EchoSkillEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

ECHO_SKILL_PATH = "./data/v1/echo_skills.tsv"


class EchoSkillTable:
    def __init__(self):
        _stat_path = Path(ECHO_SKILL_PATH)
        self.df = get_df(_stat_path)

    def search(self, id: str, col: EchoSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoSkillEnum.SKILL_ID.value)
