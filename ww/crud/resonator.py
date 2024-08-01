from pathlib import Path
from typing import List, Optional

from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.resonator_skill import ResonatorSkillTable


def get_resonator_names() -> List[str]:
    home_path = Path(RESONATOR_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_resonator_skill_ids(resonator_name: Optional[str]) -> List[str]:
    if not resonator_name:
        return []
    table = ResonatorSkillTable(resonator_name)
    names = [
        name for name in table.df[ResonatorSkillEnum.SKILL_ID.value].to_list() if name
    ]
    return names


def get_resonator_chains() -> List[str]:
    return [str(i) for i in range(7)]


def get_resonator_inherent_skills() -> List[str]:
    return ["0", "1"]
