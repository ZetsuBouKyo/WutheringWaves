from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from ww.model.buff import (
    EchoBuffEnum,
    EchoSonataBuffEnum,
    ResonatorBuffEnum,
    WeaponBuffEnum,
)
from ww.tables.base import BaseTable
from ww.tables.crud import df_to_list, get_rows
from ww.utils.pd import safe_get_df

RESONATOR_BUFF_PATH = "./data/v1/zh_tw/buff/resonator.tsv"
WEAPON_BUFF_PATH = "./data/v1/zh_tw/buff/weapon.tsv"
ECHO_BUFF_PATH = "./data/v1/zh_tw/buff/echo.tsv"
ECHO_SONATA_BUFF_PATH = "./data/v1/zh_tw/buff/echo_sonata.tsv"


def get_resonator_buff_fpath() -> Path:
    return Path(RESONATOR_BUFF_PATH)


def get_weapon_buff_fpath() -> Path:
    return Path(WEAPON_BUFF_PATH)


def get_echo_buff_fpath() -> Path:
    return Path(ECHO_BUFF_PATH)


def get_echo_sonata_buff_fpath() -> Path:
    return Path(ECHO_SONATA_BUFF_PATH)


class ResonatorBuffTable(BaseTable):
    def __init__(self):
        super().__init__(
            get_resonator_buff_fpath(), [e.value for e in ResonatorBuffEnum]
        )

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, ResonatorBuffEnum.NAME.value))


class WeaponBuffTable(BaseTable):
    def __init__(self):
        super().__init__(get_weapon_buff_fpath(), [e.value for e in WeaponBuffEnum])

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, WeaponBuffEnum.NAME.value))


class EchoBuffTable(BaseTable):
    def __init__(self):
        super().__init__(get_echo_buff_fpath(), [e.value for e in EchoBuffEnum])

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, EchoBuffEnum.NAME.value))


class EchoSonataBuffTable(BaseTable):
    def __init__(self):
        super().__init__(
            get_echo_sonata_buff_fpath(), [e.value for e in EchoSonataBuffEnum]
        )

    def get_rows(self, name: str) -> List[Dict[str, str]]:
        return df_to_list(get_rows(self.df, name, EchoSonataBuffEnum.NAME.value))
