from pathlib import Path
from typing import Optional

import pandas as pd

from ww.model.echo import EchoesEnum, EchoSonataEnum
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

        self.echo_table = EchoesTable()

        self._init_echo()

        self._update_by_resonator()
        self._update_by_weapon_stat()
        self._update_by_weapon_rank()

        self._update_by_echoes()
        self._update_by_echo_sonata()

        print(self._new_row)

    def _init_echo(self):
        self.echo_key_names = [
            CalculatedResonatorsEnum.ECHO_HP.value,
            CalculatedResonatorsEnum.ECHO_HP_P.value,
            CalculatedResonatorsEnum.ECHO_ATK.value,
            CalculatedResonatorsEnum.ECHO_ATK_P.value,
            CalculatedResonatorsEnum.ECHO_DEF.value,
            CalculatedResonatorsEnum.ECHO_DEF_P.value,
            CalculatedResonatorsEnum.ECHO_CRIT_RATE.value,
            CalculatedResonatorsEnum.ECHO_CRIT_DMG.value,
            CalculatedResonatorsEnum.ECHO_ENERGY_REGEN.value,
            CalculatedResonatorsEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_GLACIO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_FUSION_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_ELECTRO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_AERO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SPECTRO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_HAVOC_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_HEALING_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_ATK_P.value,
            CalculatedResonatorsEnum.ECHO_SONATA_ENERGY_REGEN.value,
            CalculatedResonatorsEnum.ECHO_SONATA_GLACIO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_FUSION_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_ELECTRO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_AERO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_SPECTRO_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_HAVOC_DMG_BONUS.value,
            CalculatedResonatorsEnum.ECHO_SONATA_HEALING_BONUS.value,
        ]
        for key in self.echo_key_names:
            self._new_row[key] = 0.0

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

    def _update_by_echo(self, echo_id: str):
        echo_main_hp = get_number(self.echo_table.search(echo_id, EchoesEnum.MAIN_HP))
        echo_main_atk = get_number(self.echo_table.search(echo_id, EchoesEnum.MAIN_ATK))
        echo_main_hp_p = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_HP_P)
        )
        echo_main_atk_p = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_ATK_P)
        )
        echo_main_def_p = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_DEF_P)
        )
        echo_main_crit_rate = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_CRIT_RATE)
        )
        echo_main_crit_dmg = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_CRIT_DMG)
        )
        echo_main_energy_regen = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_ENERGY_REGEN)
        )

        echo_main_glacio_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_GLACIO_DMG_BONUS)
        )
        echo_main_fusion_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_FUSION_DMG_BONUS)
        )
        echo_main_electro_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_ELECTRO_DMG_BONUS)
        )
        echo_main_aero_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_AERO_DMG_BONUS)
        )
        echo_main_spectro_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_SPECTRO_DMG_BONUS)
        )
        echo_main_havoc_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_HAVOC_DMG_BONUS)
        )
        echo_main_healing_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.MAIN_HEALING_BONUS)
        )

        echo_sub_hp = get_number(self.echo_table.search(echo_id, EchoesEnum.SUB_HP))
        echo_sub_hp_p = get_number(self.echo_table.search(echo_id, EchoesEnum.SUB_HP_P))
        echo_sub_atk = get_number(self.echo_table.search(echo_id, EchoesEnum.SUB_ATK))
        echo_sub_atk_p = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_ATK_P)
        )
        echo_sub_def = get_number(self.echo_table.search(echo_id, EchoesEnum.SUB_DEF))
        echo_sub_def_p = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_DEF_P)
        )
        echo_sub_crit_rate = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_CRIT_RATE)
        )
        echo_sub_crit_dmg = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_CRIT_DMG)
        )
        echo_sub_energy_regen = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_ENERGY_REGEN)
        )
        echo_sub_resonance_skill_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_RESONANCE_SKILL_DMG_BONUS)
        )
        echo_sub_basic_attack_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_BASIC_ATTACK_DMG_BONUS)
        )
        echo_sub_heavy_attack_dmg_bonus = get_number(
            self.echo_table.search(echo_id, EchoesEnum.SUB_HEAVY_ATTACK_DMG_BONUS)
        )
        echo_sub_resonance_liberation_dmg_bonus = get_number(
            self.echo_table.search(
                echo_id, EchoesEnum.SUB_RESONANCE_LIBERATION_DMG_BONUS
            )
        )

        self._new_row[CalculatedResonatorsEnum.ECHO_HP.value] += (
            echo_main_hp + echo_sub_hp
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_HP_P.value] += (
            echo_main_hp_p + echo_sub_hp_p
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_ATK.value] += (
            echo_main_atk + echo_sub_atk
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_ATK_P.value] += (
            echo_main_atk_p + echo_sub_atk_p
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_DEF.value] += echo_sub_def
        self._new_row[CalculatedResonatorsEnum.ECHO_DEF_P.value] += (
            echo_main_def_p + echo_sub_def_p
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_CRIT_RATE.value] += (
            echo_main_crit_rate + echo_sub_crit_rate
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_CRIT_DMG.value] += (
            echo_main_crit_dmg + echo_sub_crit_dmg
        )
        self._new_row[CalculatedResonatorsEnum.ECHO_ENERGY_REGEN.value] += (
            echo_main_energy_regen + echo_sub_energy_regen
        )

        self._new_row[
            CalculatedResonatorsEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
        ] += echo_sub_resonance_skill_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value
        ] += echo_sub_basic_attack_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value
        ] += echo_sub_heavy_attack_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value
        ] += echo_sub_resonance_liberation_dmg_bonus

        self._new_row[
            CalculatedResonatorsEnum.ECHO_GLACIO_DMG_BONUS.value
        ] += echo_main_glacio_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_FUSION_DMG_BONUS.value
        ] += echo_main_fusion_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_ELECTRO_DMG_BONUS.value
        ] += echo_main_electro_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_AERO_DMG_BONUS.value
        ] += echo_main_aero_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_SPECTRO_DMG_BONUS.value
        ] += echo_main_spectro_dmg_bonus
        self._new_row[
            CalculatedResonatorsEnum.ECHO_HAVOC_DMG_BONUS.value
        ] += echo_main_havoc_dmg_bonus

        self._new_row[
            CalculatedResonatorsEnum.ECHO_HEALING_BONUS.value
        ] += echo_main_healing_bonus

    def _update_by_echoes(self):
        self.echo_id_1 = self._old_row[ResonatorsEnum.ECHO_1]
        self.echo_id_2 = self._old_row[ResonatorsEnum.ECHO_2]
        self.echo_id_3 = self._old_row[ResonatorsEnum.ECHO_3]
        self.echo_id_4 = self._old_row[ResonatorsEnum.ECHO_4]
        self.echo_id_5 = self._old_row[ResonatorsEnum.ECHO_5]

        self._update_by_echo(self.echo_id_1)
        self._update_by_echo(self.echo_id_2)
        self._update_by_echo(self.echo_id_3)
        self._update_by_echo(self.echo_id_4)
        self._update_by_echo(self.echo_id_5)

    def _update_by_echo_sonata(self):
        sonatas = [
            self.echo_table.search(self.echo_id_1, EchoesEnum.ECHO_SONATA),
            self.echo_table.search(self.echo_id_2, EchoesEnum.ECHO_SONATA),
            self.echo_table.search(self.echo_id_3, EchoesEnum.ECHO_SONATA),
            self.echo_table.search(self.echo_id_4, EchoesEnum.ECHO_SONATA),
            self.echo_table.search(self.echo_id_5, EchoesEnum.ECHO_SONATA),
        ]

        count_sonatas = {e.value: 0 for e in EchoSonataEnum}
        for sonata in sonatas:
            if count_sonatas.get(sonata, None) is None:
                continue
            count_sonatas[sonata] += 1

        if count_sonatas[EchoSonataEnum.LINGERING_TUNES.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_ATK_P.value] += 0.1

        if count_sonatas[EchoSonataEnum.MOONLIT_CLOUDS.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_ENERGY_REGEN.value] += 0.1

        if count_sonatas[EchoSonataEnum.FREEZING_FROST.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_GLACIO_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.MOLTEN_RIFT.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_FUSION_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.VOID_THUNDER.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_ELECTRO_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.SIERRA_GALE.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_AERO_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.CELESTIAL_LIGHT.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_SPECTRO_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.SUN_SINKING_ECLIPSE.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_HAVOC_DMG_BONUS.value] += 0.1

        if count_sonatas[EchoSonataEnum.REJUVENATING_GLOW.value] >= 2:
            self._new_row[CalculatedResonatorsEnum.ECHO_HEALING_BONUS.value] += 0.1


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
    # print(resonators.head(2).T)
    # print_transpose_table("", resonators.head(2).T)
