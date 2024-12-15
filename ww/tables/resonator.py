import json
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd

from ww.locale import ZhTwEnum, _
from ww.model.resonator import (
    CalculatedResonatorModel,
    CalculatedResonatorTsvColumnEnum,
    ResonatorInformationModel,
    ResonatorStatTsvColumnEnum,
    ResonatorTsvColumnEnum,
    ResonatorTsvModel,
)
from ww.model.resonator_skill import ResonatorSkillTsvColumnEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = f"./data/v1/zh_tw/{_(ZhTwEnum.CHARACTER)}"
RESONATOR_SKILL_INFORMATION_FNAME = f"{_(ZhTwEnum.SKILL_INFORMATION)}.json"
RESONATOR_STAT_FNAME = f"{_(ZhTwEnum.STAT)}.tsv"
RESONATOR_SKILL_FNAME = f"{_(ZhTwEnum.SKILL)}.tsv"
RESONATOR_INFORMATION_FNAME = f"{_(ZhTwEnum.INFORMATION)}.json"

RESONATORS_PATH = "./cache/v1/zh_tw/custom/resonator/resonators.tsv"
CALCULATED_RESONATOR_PATH = "./cache/v1/zh_tw/output/[calculated]resonators.tsv"


def get_resonator_dir_path(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name


def get_resonator_information_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return (
        Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_SKILL_INFORMATION_FNAME
    )


def get_resonator_stat_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_STAT_FNAME


def get_resonator_skill_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_SKILL_FNAME


def get_resonator_information_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_INFORMATION_FNAME


def get_resonator_information(resonator_name: str) -> ResonatorInformationModel:
    _path = get_resonator_information_fpath(resonator_name)
    with _path.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)
    return ResonatorInformationModel(**data)


def get_resonator_element(resonator_name: str) -> str:
    info = get_resonator_information(resonator_name)
    return info.element


class ResonatorStatTable:
    def __init__(self, name):
        _path = get_resonator_stat_fpath(name)
        self.column_names = [e.value for e in ResonatorStatTsvColumnEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: ResonatorStatTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorStatTsvColumnEnum.LEVEL.value)


class ResonatorSkillTable:
    def __init__(self, name):
        _path = get_resonator_skill_fpath(name)
        self.column_names = [e.value for e in ResonatorSkillTsvColumnEnum]

        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: ResonatorSkillTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorSkillTsvColumnEnum.PRIMARY_KEY.value)

    def get_row(self, id: str) -> Optional[pd.DataFrame]:
        return get_row(self.df, id, ResonatorSkillTsvColumnEnum.PRIMARY_KEY.value)


class ResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in ResonatorTsvColumnEnum]
        self.df = safe_get_df(RESONATORS_PATH, self.column_names)

    def search(self, id: str, col: ResonatorTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorTsvColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[pd.DataFrame]:
        return get_row(self.df, id, ResonatorTsvColumnEnum.ID.value)

    def get_resonator_model(self, id: str) -> ResonatorTsvModel:
        model = ResonatorTsvModel()
        row = self.get_row(id)
        if row is None:
            return model
        row_dict = row.iloc[0].to_dict()

        for e in ResonatorTsvColumnEnum:
            value = row_dict.get(e.value, "")
            setattr(model, e.name.lower(), value)
        return model


class CalculatedResonatorsTable:
    def __init__(self):
        self.column_names = [e.value for e in CalculatedResonatorTsvColumnEnum]
        self.df = safe_get_df(CALCULATED_RESONATOR_PATH, self.column_names)

    def search(self, id: str, col: CalculatedResonatorTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, CalculatedResonatorTsvColumnEnum.ID.value)

    def get_row(self, id: str) -> Optional[pd.DataFrame]:
        return get_row(self.df, id, CalculatedResonatorTsvColumnEnum.ID.value)

    def get_calculated_resonator_model(self, id: str) -> CalculatedResonatorModel:
        model = CalculatedResonatorModel()
        row = self.get_row(id)
        if row is None:
            return model
        row_dict = row.iloc[0].to_dict()

        for e in CalculatedResonatorTsvColumnEnum:
            value = row_dict.get(e.value, "")
            setattr(model, e.name.lower(), value)
        return model
