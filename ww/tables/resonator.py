from pathlib import Path
from typing import Any, List, Optional

from ww.locale import ZhTwEnum, _
from ww.model.resonator import ResonatorStatEnum
from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = f"./data/v1/zh_tw/{_(ZhTwEnum.CHARACTER)}"
RESONATOR_INFORMATION_FNAME = f"{_(ZhTwEnum.INFORMATION)}.json"
RESONATOR_STAT_FNAME = f"{_(ZhTwEnum.STAT)}.tsv"
RESONATOR_SKILL_FNAME = f"{_(ZhTwEnum.SKILL)}.tsv"


def get_resonator_information_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_INFORMATION_FNAME


def get_resonator_dir_path(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name


def get_resonator_stat_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_STAT_FNAME


def get_resonator_skill_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_SKILL_FNAME


class ResonatorStatTable:
    def __init__(self, name):
        _path = get_resonator_stat_fpath(name)
        self.column_names = [e.value for e in ResonatorStatEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: ResonatorStatEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorStatEnum.LEVEL.value)


class ResonatorSkillTable:
    def __init__(self, name):
        _path = get_resonator_skill_fpath(name)
        self.column_names = [e.value for e in ResonatorSkillEnum]

        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: ResonatorSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorSkillEnum.PRIMARY_KEY.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, ResonatorSkillEnum.PRIMARY_KEY.value)
