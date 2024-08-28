import os
from pathlib import Path
from typing import List, Optional

from ww.model.resonator_damage_compare import ResonatorDamageCompareModel

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


def save_resonator_damage_compare(data: ResonatorDamageCompareModel):
    id = data.id
    if not id:
        return

    home_path = get_resonator_damage_compare_home_path(id)
    os.makedirs(home_path, exist_ok=True)

    fname = f"{id}.json"
    fpath = home_path / fname

    with fpath.open(mode="w", encoding="utf-8") as fp:
        data = data.model_dump_json(indent=4)
        fp.write(data)
