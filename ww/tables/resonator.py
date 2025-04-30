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
from ww.model.resonator_skill import ResonatorSkillModel, ResonatorSkillTsvColumnEnum
from ww.tables.crud import get_row, search
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_HOME_PATH = f"./data/v1/zh_tw/{_(ZhTwEnum.CHARACTER)}"
RESONATOR_INFORMATION_FNAME = f"{_(ZhTwEnum.INFORMATION)}.json"
RESONATOR_STAT_FNAME = f"{_(ZhTwEnum.STAT)}.tsv"
RESONATOR_SKILL_FNAME = f"{_(ZhTwEnum.SKILL)}.tsv"
RESONATOR_SKILL_INFORMATION_FNAME = f"{_(ZhTwEnum.SKILL_INFORMATION)}.json"

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


def get_resonator_skill_information_fpath(resonator_name: str) -> Optional[Path]:
    if not resonator_name:
        return None
    return (
        Path(RESONATOR_HOME_PATH) / resonator_name / RESONATOR_SKILL_INFORMATION_FNAME
    )


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

    # TODO: refactor
    def get_skills_model(self) -> List[ResonatorSkillModel]:
        skills = []
        for _, row in self.df.iterrows():
            skill_type = row.get(ResonatorSkillTsvColumnEnum.TYPE_ZH_TW.value, "")
            skill_name = row.get(ResonatorSkillTsvColumnEnum.PRIMARY_KEY.value, "")
            skill_bonus_type = row.get(
                ResonatorSkillTsvColumnEnum.SKILL_BONUS_TYPE.value, ""
            )
            base_attribute = row.get(ResonatorSkillTsvColumnEnum.BASE_ATTR.value, "")
            resonance_energy = row.get(
                ResonatorSkillTsvColumnEnum.RESONANCE_LIBERATION_ENERGY.value, ""
            )
            concerto_energy = row.get(
                ResonatorSkillTsvColumnEnum.RESONATING_SPIN_CONCERTO_ENERGY.value, ""
            )
            lv_1 = row.get(ResonatorSkillTsvColumnEnum.LV1.value, "")
            lv_2 = row.get(ResonatorSkillTsvColumnEnum.LV2.value, "")
            lv_3 = row.get(ResonatorSkillTsvColumnEnum.LV3.value, "")
            lv_4 = row.get(ResonatorSkillTsvColumnEnum.LV4.value, "")
            lv_5 = row.get(ResonatorSkillTsvColumnEnum.LV5.value, "")
            lv_6 = row.get(ResonatorSkillTsvColumnEnum.LV6.value, "")
            lv_7 = row.get(ResonatorSkillTsvColumnEnum.LV7.value, "")
            lv_8 = row.get(ResonatorSkillTsvColumnEnum.LV8.value, "")
            lv_9 = row.get(ResonatorSkillTsvColumnEnum.LV9.value, "")
            lv_10 = row.get(ResonatorSkillTsvColumnEnum.LV10.value, "")

            skill = ResonatorSkillModel(
                skill_type=skill_type,
                skill_name=skill_name,
                skill_bonus_type=skill_bonus_type,
                base_attribute=base_attribute,
                resonance_energy=resonance_energy,
                concerto_energy=concerto_energy,
                lv_1=lv_1,
                lv_2=lv_2,
                lv_3=lv_3,
                lv_4=lv_4,
                lv_5=lv_5,
                lv_6=lv_6,
                lv_7=lv_7,
                lv_8=lv_8,
                lv_9=lv_9,
                lv_10=lv_10,
            )

            skills.append(skill)
        return skills


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
