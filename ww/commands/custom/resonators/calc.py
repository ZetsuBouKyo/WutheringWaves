from pathlib import Path
from typing import Optional

import pandas as pd

from ww.model.resonator import ResonatorEnum
from ww.model.resonators import CalculatedResonatorsEnum, ResonatorsEnum
from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.echoes import EchoesTable
from ww.tables.resonator import ResonatorStatTable
from ww.tables.resonators import ResonatorsTable
from ww.tables.weapon import WeaponRankTable, WeaponStatTable
from ww.utils.number import get_number
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

        self.weapon_name = self._old_row[ResonatorsEnum.WEAPON_NAME]
        self.weapon_level = self._old_row[ResonatorsEnum.WEAPON_LEVEL]
        self.weapon_rank = self._old_row[ResonatorsEnum.WEAPON_RANK]

        self._update_by_resonator()
        self._update_by_weapon_stat()
        self._update_by_weapon_rank()

        self._update_by_echoes()

        print(self._new_row)

    def _update_by_resonator(self):
        resonator_name = self._old_row[ResonatorsEnum.NAME]
        resonator_level = self._old_row[ResonatorsEnum.LEVEL]

        resonator_table = ResonatorStatTable(resonator_name)
        resonator_hp = resonator_table.search(resonator_level, ResonatorEnum.HP)
        resonator_atk = resonator_table.search(resonator_level, ResonatorEnum.ATK)
        resonator_def = resonator_table.search(resonator_level, ResonatorEnum.DEF)

        self._new_row[CalculatedResonatorsEnum.HP.value] = get_number(resonator_hp)
        self._new_row[CalculatedResonatorsEnum.ATK.value] = get_number(resonator_atk)
        self._new_row[CalculatedResonatorsEnum.DEF.value] = get_number(resonator_def)

    def _update_by_weapon_stat(self):
        weapon_table = WeaponStatTable(self.weapon_name)
        weapon_atk = weapon_table.search(self.weapon_level, WeaponStatEnum.ATK)
        weapon_atk_p = weapon_table.search(self.weapon_level, WeaponStatEnum.ATK_P)
        weapon_def_p = weapon_table.search(self.weapon_level, WeaponStatEnum.DEF_P)
        weapon_hp_p = weapon_table.search(self.weapon_level, WeaponStatEnum.HP_P)
        weapon_crit_dmg = weapon_table.search(
            self.weapon_level, WeaponStatEnum.CRIT_DMG
        )
        weapon_crit_rate = weapon_table.search(
            self.weapon_level, WeaponStatEnum.CRIT_RATE
        )
        weapon_energy_regen = weapon_table.search(
            self.weapon_level, WeaponStatEnum.ENERGY_REGEN
        )

        self._new_row[CalculatedResonatorsEnum.WEAPON_ATK.value] = weapon_atk
        self._new_row[CalculatedResonatorsEnum.WEAPON_ATK_P.value] = weapon_atk_p
        self._new_row[CalculatedResonatorsEnum.WEAPON_DEF_P.value] = weapon_def_p
        self._new_row[CalculatedResonatorsEnum.WEAPON_HP_P.value] = weapon_hp_p
        self._new_row[CalculatedResonatorsEnum.WEAPON_CRIT_DMG.value] = weapon_crit_dmg
        self._new_row[CalculatedResonatorsEnum.WEAPON_CRIT_RATE.value] = (
            weapon_crit_rate
        )
        self._new_row[CalculatedResonatorsEnum.WEAPON_ENERGY_REGEN.value] = (
            weapon_energy_regen
        )

    def _update_by_weapon_rank(self):
        weapon_table = WeaponRankTable(self.weapon_name)
        weapon_rank_atk_p = weapon_table.search(self.weapon_rank, WeaponRankEnum.ATK_P)
        weapon_rank_attribute_dmg_bonus = weapon_table.search(
            self.weapon_rank, WeaponRankEnum.ATTRIBUTE_DMG_BONUS
        )
        weapon_rank_energy_regen = weapon_table.search(
            self.weapon_rank, WeaponRankEnum.ENERGY_REGEN
        )

        self._new_row[CalculatedResonatorsEnum.WEAPON_RANK_ATK_P.value] = (
            weapon_rank_atk_p
        )
        self._new_row[
            CalculatedResonatorsEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
        ] = weapon_rank_attribute_dmg_bonus
        self._new_row[CalculatedResonatorsEnum.WEAPON_RANK_ENERGY_REGEN.value] = (
            weapon_rank_energy_regen
        )

    def _update_by_echo(self, echo_name: str):
        echo_table = EchoesTable(echo_name)

    def _update_by_echoes(self):
        pass


def calc():
    resonators_table = ResonatorsTable()
    resonators_df = resonators_table.df

    echoes_table = EchoesTable()
    echoes_df = echoes_table.df

    df_calculated_resonators_cols = [e.value for e in ResonatorsEnum]

    df_calculated_resonators = pd.DataFrame(columns=df_calculated_resonators_cols)

    for _, row in resonators_df.iterrows():
        new_resonator = CalculatedResonator(row)
        break

    # html = Path(CALCULATED_RESONATOR_HTML_PATH)
    # df.to_html(html)

    # print(df.transpose())

    # print(resonators.head(2).T)
    # print_transpose_table("", resonators.head(2).T)
