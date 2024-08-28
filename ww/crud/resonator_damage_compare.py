from pathlib import Path
from typing import List, Optional

RESONATOR_DAMAGE_COMPARE_HOME_PATH = "./cache/v1/zh_tw/custom/resonator_damage_compare"


def get_resonator_damage_compare_home_path(id: str) -> Optional[Path]:
    if not id:
        return None
    return Path(RESONATOR_DAMAGE_COMPARE_HOME_PATH) / id


def get_resonator_damage_compare_ids(
    home_path: str = RESONATOR_DAMAGE_COMPARE_HOME_PATH,
) -> List[str]:
    home_path = Path(home_path)
    names = [p.stem for p in home_path.glob("*.json")]
    return names
