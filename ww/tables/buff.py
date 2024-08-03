from pathlib import Path
from typing import Any, List, Optional

import pandas as pd

from ww.model.buff import (
    EchoBuffEnum,
    EchoSonataBuffEnum,
    ResonatorBuffEnum,
    WeaponBuffEnum,
)
from ww.tables.crud import get_rows
from ww.utils.pd import safe_get_df

RESONATOR_BUFF_PATH = "./data/v1/buff/resonator.tsv"
WEAPON_BUFF_PATH = "./data/v1/buff/weapon.tsv"
ECHO_BUFF_PATH = "./data/v1/buff/echo.tsv"
ECHO_SONATA_BUFF_PATH = "./data/v1/buff/echo_sonata.tsv"


class ResonatorBuffTable:
    def __init__(self):
        p = Path(RESONATOR_BUFF_PATH)
        column_names = [e.value for e in ResonatorBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> pd.DataFrame:
        return get_rows(self.df, name, ResonatorBuffEnum.RESONATOR_NAME.value)


class WeaponBuffTable:
    def __init__(self):
        p = Path(WEAPON_BUFF_PATH)
        column_names = [e.value for e in WeaponBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> pd.DataFrame:
        return get_rows(self.df, name, WeaponBuffEnum.WEAPON_NAME.value)


class EchoBuffTable:
    def __init__(self):
        p = Path(ECHO_BUFF_PATH)
        column_names = [e.value for e in EchoBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> pd.DataFrame:
        return get_rows(self.df, name, EchoBuffEnum.ECHO_NAME.value)


class EchoSonataBuffTable:
    def __init__(self):
        p = Path(ECHO_SONATA_BUFF_PATH)
        column_names = [e.value for e in EchoSonataBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> pd.DataFrame:
        return get_rows(self.df, name, EchoSonataBuffEnum.ECHO_SONATA_NAME.value)
