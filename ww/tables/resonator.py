from pathlib import Path
from typing import Any, List, Optional

from ww.locale import ZhTwEnum, _
from ww.model.resonator import (
    CalculatedResonatorColumnEnum,
    CalculatedResonatorModel,
    ResonatorColumnEnum,
    ResonatorStatColumnEnum,
)
from ww.model.resonator_skill import ResonatorSkillEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = f"./data/v1/zh_tw/{_(ZhTwEnum.CHARACTER)}"
RESONATOR_INFORMATION_FNAME = f"{_(ZhTwEnum.INFORMATION)}.json"
RESONATOR_STAT_FNAME = f"{_(ZhTwEnum.STAT)}.tsv"
RESONATOR_SKILL_FNAME = f"{_(ZhTwEnum.SKILL)}.tsv"

RESONATORS_PATH = "./cache/v1/zh_tw/custom/resonator/resonators.tsv"
CALCULATED_RESONATOR_PATH = "./cache/v1/zh_tw/output/[calculated]resonators.tsv"


def get_resonator_dir_path(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name


def get_resonator_information_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_INFORMATION_FNAME


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
        self.column_names = [e.value for e in ResonatorStatColumnEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: ResonatorStatColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorStatColumnEnum.LEVEL.value)


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


class ResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in ResonatorColumnEnum]
        self.df = safe_get_df(RESONATORS_PATH, self.column_names)

    def search(self, id: str, col: ResonatorColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, ResonatorColumnEnum.ID.value)


class CalculatedResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in CalculatedResonatorColumnEnum]
        self.df = safe_get_df(CALCULATED_RESONATOR_PATH, self.column_names)

    def search(self, id: str, col: CalculatedResonatorColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, CalculatedResonatorColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[List[Any]]:
        return get_row(self.df, id, CalculatedResonatorColumnEnum.ID.value)

    def get_calculated_resonator_model(self, id: str) -> CalculatedResonatorModel:
        row = self.get_row(id)
