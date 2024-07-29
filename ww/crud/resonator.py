from pathlib import Path
from typing import List

from ww.tables.resonator import RESONATOR_HOME_PATH


def get_resonator_names() -> List[str]:
    home_path = Path(RESONATOR_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_resonator_chains() -> List[str]:
    return [str(i) for i in range(7)]


def get_resonator_inherent_skills() -> List[str]:
    return ["0", "1"]
