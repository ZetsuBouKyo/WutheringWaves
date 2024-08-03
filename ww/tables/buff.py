from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from ww.model.buff import (
    EchoBuffEnum,
    EchoSonataBuffEnum,
    ResonatorBuffEnum,
    WeaponBuffEnum,
)
from ww.tables.crud import df_to_list, get_rows
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

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, ResonatorBuffEnum.NAME.value))


class WeaponBuffTable:
    def __init__(self):
        p = Path(WEAPON_BUFF_PATH)
        column_names = [e.value for e in WeaponBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, WeaponBuffEnum.NAME.value))


class EchoBuffTable:
    def __init__(self):
        p = Path(ECHO_BUFF_PATH)
        column_names = [e.value for e in EchoBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, EchoBuffEnum.NAME.value))


class EchoSonataBuffTable:
    def __init__(self):
        p = Path(ECHO_SONATA_BUFF_PATH)
        column_names = [e.value for e in EchoSonataBuffEnum]
        self.df = safe_get_df(p, column_names)

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, EchoSonataBuffEnum.NAME.value))
