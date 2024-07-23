from pathlib import Path
from typing import Any, List, Optional

from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_df

RESONATOR_HOME_PATH = "./data/角色"
RESONATOR_SKILL_FNAME = "技能.tsv"


class ResonatorSkillTable:
    def __init__(self, name):
        _stat_path = Path(RESONATOR_HOME_PATH) / name / RESONATOR_SKILL_FNAME
        self.df = get_df(_stat_path)

    def search(self, id: str, col: ResonatorSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorSkillEnum.SKILL_ID.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, ResonatorSkillEnum.SKILL_ID.value)
