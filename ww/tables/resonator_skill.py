from pathlib import Path
from typing import Any, List, Optional

from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = "./data/v1/角色"
RESONATOR_SKILL_FNAME = "技能.tsv"


def get_resonator_skill_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_SKILL_FNAME


class ResonatorSkillTable:
    def __init__(self, name):
        _path = get_resonator_skill_fpath(name)
        column_names = [e.value for e in ResonatorSkillEnum]

        if _path is not None:
            self.df = safe_get_df(_path, column_names)
        else:
            self.df = get_empty_df(column_names)

    def search(self, id: str, col: ResonatorSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorSkillEnum.PRIMARY_KEY.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, ResonatorSkillEnum.PRIMARY_KEY.value)
