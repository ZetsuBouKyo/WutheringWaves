import json
import os
from pathlib import Path
from typing import List, Optional

from ww.model.damage_compare import DamageCompareModel

TEAM_DAMAGE_COMPARE_HOME_PATH = "./cache/v1/zh_tw/custom/team_damage_compare"


def get_team_damage_compare_fpath(id: str) -> Optional[Path]:
    if not id:
        return None
    return Path(TEAM_DAMAGE_COMPARE_HOME_PATH) / f"{id}.json"


def get_team_damage_compare_ids(
    home_path: str = TEAM_DAMAGE_COMPARE_HOME_PATH,
) -> List[str]:
    home_path = Path(home_path)
    names = [p.stem for p in home_path.glob("*.json")]
    return names


def get_team_damage_compare(id: str) -> Optional[DamageCompareModel]:
    fpath = get_team_damage_compare_fpath(id)
    if not fpath.exists():
        return
    with fpath.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
    return DamageCompareModel(**data)


def save_team_damage_compare(data: DamageCompareModel):
    id = data.id
    if not id:
        return

    fpath = get_team_damage_compare_fpath(id)
    os.makedirs(fpath.parent, exist_ok=True)

    with fpath.open(mode="w", encoding="utf-8") as fp:
        data = data.model_dump_json(indent=4)
        fp.write(data)


def delete_team_damage_compare(id: str) -> bool:
    fpath = get_team_damage_compare_fpath(id)
    if not fpath.is_dir() and fpath.exists():
        fpath.unlink()
        return True
    return False
