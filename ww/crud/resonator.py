from pathlib import Path
from typing import List, Optional

import pandas as pd

from ww.model.resonator_skill import ResonatorSkillEnum
from ww.model.resonators import ResonatorsEnum
from ww.tables.echo_skill import EchoSkillEnum, EchoSkillTable
from ww.tables.resonator import RESONATOR_HOME_PATH, ResonatorStatTable
from ww.tables.resonator_skill import ResonatorSkillTable
from ww.tables.resonators import ResonatorsTable


def get_resonator_names() -> List[str]:
    home_path = Path(RESONATOR_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_resonator_ids() -> List[str]:
    resonators_table = ResonatorsTable()
    names = [name for name in resonators_table.df[ResonatorsEnum.ID].to_list() if name]
    return names


def get_resonator_skill_ids(resonator_name: Optional[str]) -> List[str]:
    if not resonator_name:
        return []
    table = ResonatorSkillTable(resonator_name)
    names = [
        name
        for name in table.df[ResonatorSkillEnum.PRIMARY_KEY.value].to_list()
        if name
    ]
    return names


def get_resonator_and_echo_skill_ids(resonator_name: Optional[str]) -> List[str]:
    resonator_skill_ids = get_resonator_skill_ids(resonator_name)
    echo_skill_table = EchoSkillTable()
    echo_skill_ids = [
        name
        for name in echo_skill_table.df[EchoSkillEnum.SKILL_ID.value].to_list()
        if name
    ]
    return resonator_skill_ids + echo_skill_ids


def get_resonator_chains() -> List[str]:
    return [str(i) for i in range(7)]


def get_resonator_inherent_skills() -> List[str]:
    return ["0", "1"]


RESONATOR_ICON_HOME_PATH = "./cache/v1/assets/resonator/icon"


def get_resonator_icon_path(resonator_name: str) -> Optional[str]:
    path = Path(RESONATOR_ICON_HOME_PATH) / f"{resonator_name}.png"
    if path.is_dir() or not path.exists():
        return
    return str(path)


def get_resonator_stat_df(resonator_name: str) -> pd.DataFrame:
    return ResonatorStatTable(resonator_name).df
