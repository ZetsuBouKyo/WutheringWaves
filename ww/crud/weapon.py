from pathlib import Path
from typing import List

from ww.tables.weapon import WEAPON_HOME_PATH


def get_weapon_names() -> List[str]:
    home_path = Path(WEAPON_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_weapon_ranks() -> List[str]:
    ranks = [str(i) for i in range(1, 6)]
    return ranks
