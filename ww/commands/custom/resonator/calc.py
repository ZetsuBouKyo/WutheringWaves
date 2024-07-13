from pathlib import Path
from typing import Optional

import pandas as pd

from ww.model.resonator import CalculatedResonatorEnum, ResonatorEnum
from ww.utils.pd import get_df

ECHO_PATH = "./data/自訂/聲骸"

CACHE_PATH = "./cache"
CALCULATED_RESONATOR_PATH = "./data/自訂/[計算用]角色"
CALCULATED_RESONATOR_HTML_PATH = "./cache/[計算用]角色.html"

RESONATOR_HOME_PATH = "./data/角色"
RESONATOR_STAT = "屬性"


def get_custom_echos() -> pd.DataFrame:
    return get_df(ECHO_PATH)


def get_custom_resonator_stat(name: str) -> Optional[pd.DataFrame]:
    p = Path(RESONATOR_HOME_PATH) / name / RESONATOR_STAT
    if not p.exists():
        return None
    return get_df(p)


class CalculatedResonator:
    def __init__(self, row):
        self._old_row = row
        self._new_row = {}

    def _update_by_df_resonator(self):
        self.resonator_name = self._old_row[ResonatorEnum.NAME]
        self._new_row[CalculatedResonatorEnum.NAME.value] = self.resonator_name

        self.resonator_level = self._old_row[ResonatorEnum.LEVEL]
        self._new_row[CalculatedResonatorEnum.LEVEL.value] = self.resonator_level


def calc():
    df_resonators = get_custom_resonators()
    df_echos = get_custom_echos()

    df_calculated_resonators_cols = [e.value for e in ResonatorEnum]

    df_calculated_resonators = pd.DataFrame(columns=df_calculated_resonators_cols)

    for _, row in df_resonators.iterrows():
        new_resonator = CalculatedResonator(row)
        resonator_name = row[ResonatorEnum.NAME]
        print(resonator_name)
        break

    # html = Path(CALCULATED_RESONATOR_HTML_PATH)
    # df.to_html(html)

    # print(df.transpose())

    # print(resonators.head(2).T)
    # print_transpose_table("", resonators.head(2).T)
