import os
from collections import OrderedDict
from pathlib import Path
from typing import Callable, Dict, List, Optional

import pandas as pd

from ww.locale import ZhTwEnum, _
from ww.model.echo import EchoSonataEnum, ResonatorEchoTsvColumnEnum
from ww.model.resonator import (
    CalculatedResonatorTsvColumnEnum,
    ResonatorStatTsvColumnEnum,
    ResonatorTsvColumnEnum,
)
from ww.model.weapon import WeaponRankEnum, WeaponStatEnum
from ww.tables.echo import EchoesTable
from ww.tables.resonator import (
    CALCULATED_RESONATOR_PATH,
    CalculatedResonatorsTable,
    ResonatorsTable,
    ResonatorStatTable,
)
from ww.tables.weapon import WeaponRankTable, WeaponStatTable
from ww.utils.number import get_number
from ww.utils.pd import get_df

RESONATOR_HOME_PATH = f"./data/v1/zh_tw/{_(ZhTwEnum.CHARACTER)}"


def get_custom_resonator_stat(name: str) -> Optional[pd.DataFrame]:
    p = Path(RESONATOR_HOME_PATH) / name / f"{_(ZhTwEnum.STAT)}"
    if not p.exists():
        return None
    return get_df(p)


class CalculatedResonator:
    def __init__(self, row):
        self._old_row = row
        self._new_row = {}

        self.weapon_name = self._old_row[ResonatorTsvColumnEnum.WEAPON_NAME]
        self.weapon_level = self._old_row[ResonatorTsvColumnEnum.WEAPON_LEVEL]
        self.weapon_rank = self._old_row[ResonatorTsvColumnEnum.WEAPON_RANK]

        self.echoes_table = EchoesTable()

    def calculate(self):
        self._init()
        self._init_base()
        self._init_calculated()
        self._init_echo()

        self._update_by_resonator()
        self._update_by_weapon_stat()
        self._update_by_weapon_rank()

        self._update_by_echoes()
        self._update_by_echo_sonata()

        self._update_calculated()

    def get_row_dict(self):
        return self._new_row

    def _init(self):
        self._new_row[CalculatedResonatorTsvColumnEnum.ID.value] = self._old_row[
            ResonatorTsvColumnEnum.ID
        ]

    def _init_base(self):
        self._new_row[CalculatedResonatorTsvColumnEnum.BASE_CRIT_RATE.value] = (
            get_number("0.05")
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.BASE_CRIT_DMG.value] = (
            get_number("1.5")
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.BASE_ENERGY_REGEN.value] = (
            get_number("1.0")
        )

    def _init_calculated(self):
        self.calculated_key_names = [
            CalculatedResonatorTsvColumnEnum.CALCULATED_HP.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_HP_P.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_ATK.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_ATK_P.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_DEF.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_DEF_P.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_RATE.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_DMG.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_ENERGY_REGEN.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_RESONANCE_SKILL_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_BASIC_ATTACK_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_HEAVY_ATTACK_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_RESONANCE_LIBERATION_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_PHYSICAL_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_GLACIO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_FUSION_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_ELECTRO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_AERO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_SPECTRO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_HAVOC_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_PHYSICAL_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_GLACIO_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_FUSION_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_ELECTRO_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_AERO_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_SPECTRO_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_HAVOC_DMG_RES.value,
            CalculatedResonatorTsvColumnEnum.CALCULATED_HEALING_BONUS.value,
        ]
        for key in self.calculated_key_names:
            self._new_row[key] = get_number("0.0")

    def _init_echo(self):
        self.echo_key_1 = [
            CalculatedResonatorTsvColumnEnum.ECHO_1.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SONATA_1.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SONATA_2.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SONATA_3.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SONATA_4.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SONATA_5.value,
        ]
        for key in self.echo_key_1:
            self._new_row[key] = ""

        self.echo_key_2 = [
            CalculatedResonatorTsvColumnEnum.ECHO_HP.value,
            CalculatedResonatorTsvColumnEnum.ECHO_HP_P.value,
            CalculatedResonatorTsvColumnEnum.ECHO_ATK.value,
            CalculatedResonatorTsvColumnEnum.ECHO_ATK_P.value,
            CalculatedResonatorTsvColumnEnum.ECHO_DEF.value,
            CalculatedResonatorTsvColumnEnum.ECHO_DEF_P.value,
            CalculatedResonatorTsvColumnEnum.ECHO_CRIT_RATE.value,
            CalculatedResonatorTsvColumnEnum.ECHO_CRIT_DMG.value,
            CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value,
            CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_ELECTRO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_HAVOC_DMG_BONUS.value,
            CalculatedResonatorTsvColumnEnum.ECHO_HEALING_BONUS.value,
        ]
        for key in self.echo_key_2:
            self._new_row[key] = get_number("0.0")

    def _update_by_resonator(self):
        resonator_name = self._old_row[ResonatorTsvColumnEnum.NAME]
        resonator_level = self._old_row[ResonatorTsvColumnEnum.LEVEL]

        resonator_table = ResonatorStatTable(resonator_name)
        resonator_hp = resonator_table.search(
            resonator_level, ResonatorStatTsvColumnEnum.HP
        )
        resonator_atk = resonator_table.search(
            resonator_level, ResonatorStatTsvColumnEnum.ATK
        )
        resonator_def = resonator_table.search(
            resonator_level, ResonatorStatTsvColumnEnum.DEF
        )

        self._new_row[CalculatedResonatorTsvColumnEnum.NAME.value] = resonator_name

        self._new_row[CalculatedResonatorTsvColumnEnum.HP.value] = get_number(
            resonator_hp
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ATTACK.value] = get_number(
            resonator_atk
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.DEFENSE.value] = get_number(
            resonator_def
        )

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

        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ATK.value] = get_number(
            weapon_atk
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ATK_P.value] = get_number(
            weapon_atk_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_DEF_P.value] = get_number(
            weapon_def_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_HP_P.value] = get_number(
            weapon_hp_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_CRIT_DMG.value] = (
            get_number(weapon_crit_dmg)
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_CRIT_RATE.value] = (
            get_number(weapon_crit_rate)
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ENERGY_REGEN.value] = (
            get_number(weapon_energy_regen)
        )

    def _update_by_weapon_rank(self):
        weapon_table = WeaponRankTable(self.weapon_name)
        weapon_rank_atk_p = get_number(
            weapon_table.search(self.weapon_rank, WeaponRankEnum.ATK_P)
        )
        weapon_rank_hp_p = get_number(
            weapon_table.search(self.weapon_rank, WeaponRankEnum.HP_P)
        )
        weapon_rank_crit_rate = get_number(
            weapon_table.search(self.weapon_rank, WeaponRankEnum.CRIT_RATE)
        )
        weapon_rank_attribute_dmg_bonus = get_number(
            weapon_table.search(self.weapon_rank, WeaponRankEnum.ATTRIBUTE_DMG_BONUS)
        )
        weapon_rank_energy_regen = get_number(
            weapon_table.search(self.weapon_rank, WeaponRankEnum.ENERGY_REGEN)
        )

        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATK_P.value] = (
            weapon_rank_atk_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_RANK_HP_P.value] = (
            weapon_rank_hp_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_RANK_CRIT_RATE.value] = (
            weapon_rank_crit_rate
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
        ] = weapon_rank_attribute_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ENERGY_REGEN.value
        ] = weapon_rank_energy_regen

    def _update_by_echo_1(self, echo_id: str):
        # Name
        echo_name = self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.NAME)

        if echo_name == _(ZhTwEnum.ECHO_SENTRY_CONSTRUCT):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value
            ] += get_number("0.12")

            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_NIGHTMARE_INFERNO_RIDER):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ] += get_number("0.12")

            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_NIGHTMARE_THUNDERING_MEPHIS):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ELECTRO_DMG_BONUS.value
            ] += get_number("0.12")

            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_NIGHTMARE_MOURNING_AIX):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_DRAGON_OF_DIRGE):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ] += get_number("0.12")

            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_CAPITANEUS):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
            ] += get_number("0.12")

            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_REMINISCENCE_FLEURDELYS):
            resonator_name = self._new_row[CalculatedResonatorTsvColumnEnum.NAME.value]
            if resonator_name == _(ZhTwEnum.RESONATOR_AERO) or resonator_name == _(
                ZhTwEnum.RESONATOR_CARTETHYIA
            ):
                self._new_row[
                    CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
                ] += get_number("0.1")
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.1")
        elif echo_name == _(ZhTwEnum.ECHO_NIGHTMARES_KELPIE):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value
            ] += get_number("0.12")
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_LIONESS_OF_GLORY):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ] += get_number("0.12")
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value
            ] += get_number("0.12")
        elif echo_name == _(ZhTwEnum.ECHO_NIGHTMARE_FEILIAN_BERINGAL):
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.12")
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value
            ] += get_number("0.12")

    def _update_by_echo(self, echo_id: str, index: int):
        # Name
        echo_name = self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.NAME)
        echo_sonata = self.echoes_table.search(
            echo_id, ResonatorEchoTsvColumnEnum.ECHO_SONATA
        )
        echo_n = getattr(CalculatedResonatorTsvColumnEnum, f"ECHO_{index}", None)
        if echo_n is not None:
            self._new_row[echo_n.value] = echo_name

        # Sonata
        echo_enum = getattr(
            CalculatedResonatorTsvColumnEnum, f"ECHO_SONATA_{index}", None
        )
        if echo_enum is not None:
            self._new_row[echo_enum.value] = echo_sonata

        # Value
        echo_main_hp = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_HP)
        )
        echo_main_atk = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_ATK)
        )
        echo_main_hp_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_HP_P)
        )
        echo_main_atk_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_ATK_P)
        )
        echo_main_def_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_DEF_P)
        )
        echo_main_crit_rate = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_CRIT_RATE)
        )
        echo_main_crit_dmg = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.MAIN_CRIT_DMG)
        )
        echo_main_energy_regen = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_ENERGY_REGEN
            )
        )

        echo_main_glacio_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_GLACIO_DMG_BONUS
            )
        )
        echo_main_fusion_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_FUSION_DMG_BONUS
            )
        )
        echo_main_electro_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_ELECTRO_DMG_BONUS
            )
        )
        echo_main_aero_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_AERO_DMG_BONUS
            )
        )
        echo_main_spectro_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_SPECTRO_DMG_BONUS
            )
        )
        echo_main_havoc_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_HAVOC_DMG_BONUS
            )
        )
        echo_main_healing_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.MAIN_HEALING_BONUS
            )
        )

        echo_sub_hp = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_HP)
        )
        echo_sub_hp_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_HP_P)
        )
        echo_sub_atk = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_ATK)
        )
        echo_sub_atk_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_ATK_P)
        )
        echo_sub_def = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_DEF)
        )
        echo_sub_def_p = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_DEF_P)
        )
        echo_sub_crit_rate = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_CRIT_RATE)
        )
        echo_sub_crit_dmg = get_number(
            self.echoes_table.search(echo_id, ResonatorEchoTsvColumnEnum.SUB_CRIT_DMG)
        )
        echo_sub_energy_regen = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.SUB_ENERGY_REGEN
            )
        )
        echo_sub_resonance_skill_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.SUB_RESONANCE_SKILL_DMG_BONUS
            )
        )
        echo_sub_basic_attack_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.SUB_BASIC_ATTACK_DMG_BONUS
            )
        )
        echo_sub_heavy_attack_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.SUB_HEAVY_ATTACK_DMG_BONUS
            )
        )
        echo_sub_resonance_liberation_dmg_bonus = get_number(
            self.echoes_table.search(
                echo_id, ResonatorEchoTsvColumnEnum.SUB_RESONANCE_LIBERATION_DMG_BONUS
            )
        )

        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HP.value] += (
            echo_main_hp + echo_sub_hp
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HP_P.value] += (
            echo_main_hp_p + echo_sub_hp_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_ATK.value] += (
            echo_main_atk + echo_sub_atk
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_ATK_P.value] += (
            echo_main_atk_p + echo_sub_atk_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_DEF.value] += echo_sub_def
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_DEF_P.value] += (
            echo_main_def_p + echo_sub_def_p
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_CRIT_RATE.value] += (
            echo_main_crit_rate + echo_sub_crit_rate
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_CRIT_DMG.value] += (
            echo_main_crit_dmg + echo_sub_crit_dmg
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value] += (
            echo_main_energy_regen + echo_sub_energy_regen
        )

        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
        ] += echo_sub_resonance_skill_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value
        ] += echo_sub_basic_attack_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value
        ] += echo_sub_heavy_attack_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value
        ] += echo_sub_resonance_liberation_dmg_bonus

        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value
        ] += echo_main_glacio_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
        ] += echo_main_fusion_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_ELECTRO_DMG_BONUS.value
        ] += echo_main_electro_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
        ] += echo_main_aero_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
        ] += echo_main_spectro_dmg_bonus
        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_HAVOC_DMG_BONUS.value
        ] += echo_main_havoc_dmg_bonus

        self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_HEALING_BONUS.value
        ] += echo_main_healing_bonus

    def _update_by_echoes(self):
        self.echo_id_1 = self._old_row[ResonatorTsvColumnEnum.ECHO_1]
        self.echo_id_2 = self._old_row[ResonatorTsvColumnEnum.ECHO_2]
        self.echo_id_3 = self._old_row[ResonatorTsvColumnEnum.ECHO_3]
        self.echo_id_4 = self._old_row[ResonatorTsvColumnEnum.ECHO_4]
        self.echo_id_5 = self._old_row[ResonatorTsvColumnEnum.ECHO_5]

        self._update_by_echo_1(self.echo_id_1)
        self._update_by_echo(self.echo_id_1, 1)
        self._update_by_echo(self.echo_id_2, 2)
        self._update_by_echo(self.echo_id_3, 3)
        self._update_by_echo(self.echo_id_4, 4)
        self._update_by_echo(self.echo_id_5, 5)

    def _update_by_echo_sonata(self):
        sonatas = [
            self.echoes_table.search(
                self.echo_id_1, ResonatorEchoTsvColumnEnum.ECHO_SONATA
            ),
            self.echoes_table.search(
                self.echo_id_2, ResonatorEchoTsvColumnEnum.ECHO_SONATA
            ),
            self.echoes_table.search(
                self.echo_id_3, ResonatorEchoTsvColumnEnum.ECHO_SONATA
            ),
            self.echoes_table.search(
                self.echo_id_4, ResonatorEchoTsvColumnEnum.ECHO_SONATA
            ),
            self.echoes_table.search(
                self.echo_id_5, ResonatorEchoTsvColumnEnum.ECHO_SONATA
            ),
        ]

        count_sonatas = {e.value: 0 for e in EchoSonataEnum}
        for sonata in sonatas:
            if count_sonatas.get(sonata, None) is None:
                continue
            count_sonatas[sonata] += 1

        if count_sonatas[EchoSonataEnum.LINGERING_TUNES.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ATK_P.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.MOONLIT_CLOUDS.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.FREEZING_FROST.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.MOLTEN_RIFT.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.VOID_THUNDER.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ELECTRO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.SIERRA_GALE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.CELESTIAL_LIGHT.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.SUN_SINKING_ECLIPSE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HAVOC_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.REJUVENATING_GLOW.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HEALING_BONUS.value
            ] += get_number("0.1")

        # 2.0
        if count_sonatas[EchoSonataEnum.FROSTY_RESOLVE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
            ] += get_number("0.12")

        if count_sonatas[EchoSonataEnum.ETERNAL_RADIANCE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.MIDNIGHT_VEIL.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HAVOC_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.EMPYREAN_ANTHEM.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.TIDEBREAKING_COURAGE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.GUSTS_OF_WELKIN.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.WINDWARD_PILGRIMAGE.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value
            ] += get_number("0.1")

        if count_sonatas[EchoSonataEnum.FLAMING_CLAWPRINT.value] >= 2:
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ] += get_number("0.1")

    def _update_calculated(self):
        # HP Percentage
        stat_bonus_hp_p = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_HP_P]
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_HP_P.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_HP_P.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_RANK_HP_P.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HP_P.value]
            + stat_bonus_hp_p
        )

        # HP
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_HP.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.HP.value]
            * (
                get_number("1.0")
                + self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_HP_P.value]
            )
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HP.value]
        )

        # ATK Percentage
        stat_bonus_atk_p = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_ATK_P]
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_ATK_P.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ATK_P.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATK_P.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_ATK_P.value]
            + stat_bonus_atk_p
        )

        # ATK
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_ATK.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.ATTACK.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ATK.value]
        ) * (
            get_number("1.0")
            + self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_ATK_P.value]
        ) + self._new_row[
            CalculatedResonatorTsvColumnEnum.ECHO_ATK.value
        ]

        # DEF Percentage
        stat_bonus_def_p = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_DEF_P]
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_DEF_P.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_DEF_P.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_DEF_P.value]
            + stat_bonus_def_p
        )

        # DEF
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_DEF.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.DEFENSE.value]
            * (
                get_number("1.0")
                + self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_DEF_P.value]
            )
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_DEF.value]
        )

        # CRIT Rate
        stat_bonus_crit_rate = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_RATE]
        )
        crit_rate = (
            self._new_row[CalculatedResonatorTsvColumnEnum.BASE_CRIT_RATE.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_CRIT_RATE.value]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_CRIT_RATE.value
            ]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_CRIT_RATE.value]
            + stat_bonus_crit_rate
        )
        if crit_rate >= get_number("1.0"):
            crit_rate = get_number("1.0")
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_RATE.value] = (
            crit_rate
        )

        # CRIT DMG
        stat_bonus_crit_dmg = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_DMG]
        )
        self._new_row[CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_DMG.value] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.BASE_CRIT_DMG.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_CRIT_DMG.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_CRIT_DMG.value]
            + stat_bonus_crit_dmg
        )

        # Energy Regen
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_ENERGY_REGEN.value
        ] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.BASE_ENERGY_REGEN.value]
            + self._new_row[CalculatedResonatorTsvColumnEnum.WEAPON_ENERGY_REGEN.value]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ENERGY_REGEN.value
            ]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_ENERGY_REGEN.value]
        )

        # Resonance Skill DMG Bonus
        stat_bonus_resonance_skill_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_SKILL_BONUS.value]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_RESONANCE_SKILL_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_SKILL_DMG_BONUS.value
            ]
            + stat_bonus_resonance_skill_bonus
        )

        # Basic Attack DMG Bonus
        stat_bonus_basic_attack_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_BASIC_ATTACK_BONUS.value]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_BASIC_ATTACK_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_BASIC_ATTACK_DMG_BONUS.value
            ]
            + stat_bonus_basic_attack_bonus
        )

        # Heavy Attack DMG Bonus
        stat_bonus_heavy_attack_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_HEAVY_ATTACK_BONUS.value]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_HEAVY_ATTACK_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_HEAVY_ATTACK_DMG_BONUS.value
            ]
            + stat_bonus_heavy_attack_bonus
        )

        # Resonance Liberation DMG Bonus
        stat_bonus_resonance_liberation_bonus = get_number(
            self._old_row[
                ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_LIBERATION_BONUS.value
            ]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_RESONANCE_LIBERATION_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_RESONANCE_LIBERATION_DMG_BONUS.value
            ]
            + stat_bonus_resonance_liberation_bonus
        )

        # Glacio DMG Bonus
        stat_bonus_glacio_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_GLACIO_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_GLACIO_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_GLACIO_DMG_BONUS.value
            ]
            + stat_bonus_glacio_dmg_bonus
        )

        # Fusion DMG Bonus
        stat_bonus_fusion_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_FUSION_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_FUSION_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_FUSION_DMG_BONUS.value
            ]
            + stat_bonus_fusion_dmg_bonus
        )

        # Electro DMG Bonus
        stat_bonus_electro_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_ELECTRO_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_ELECTRO_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_ELECTRO_DMG_BONUS.value
            ]
            + stat_bonus_electro_dmg_bonus
        )

        # Aero DMG Bonus
        stat_bonus_aero_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_AERO_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_AERO_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_AERO_DMG_BONUS.value]
            + stat_bonus_aero_dmg_bonus
        )

        # Spectro DMG Bonus
        stat_bonus_spectro_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_SPECTRO_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_SPECTRO_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[
                CalculatedResonatorTsvColumnEnum.ECHO_SPECTRO_DMG_BONUS.value
            ]
            + stat_bonus_spectro_dmg_bonus
        )

        # Havoc DMG Bonus
        stat_bonus_havoc_dmg_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_HAVOC_DMG_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_HAVOC_DMG_BONUS.value
        ] = (
            self._new_row[
                CalculatedResonatorTsvColumnEnum.WEAPON_RANK_ATTRIBUTE_DMG_BONUS.value
            ]
            + self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HAVOC_DMG_BONUS.value]
            + stat_bonus_havoc_dmg_bonus
        )

        # Healing Bonus
        stat_bonus_healing_bonus = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_HEALING_BONUS]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_HEALING_BONUS.value
        ] = (
            self._new_row[CalculatedResonatorTsvColumnEnum.ECHO_HEALING_BONUS.value]
            + stat_bonus_healing_bonus
        )

        # Physical DMG RES
        stat_bonus_physical_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_PHYSICAL_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_PHYSICAL_DMG_RES.value
        ] = stat_bonus_physical_dmg_res

        # Glacio DMG RES
        stat_bonus_glacio_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_GLACIO_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_GLACIO_DMG_RES.value
        ] = stat_bonus_glacio_dmg_res

        # Fusion DMG RES
        stat_bonus_fusion_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_FUSION_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_FUSION_DMG_RES.value
        ] = stat_bonus_fusion_dmg_res

        # Electro DMG RES
        stat_bonus_electro_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_ELECTRO_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_ELECTRO_DMG_RES.value
        ] = stat_bonus_electro_dmg_res

        # Aero DMG RES
        stat_bonus_aero_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_AERO_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_AERO_DMG_RES.value
        ] = stat_bonus_aero_dmg_res

        # Spectro DMG RES
        stat_bonus_spectro_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_SPECTRO_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_SPECTRO_DMG_RES.value
        ] = stat_bonus_spectro_dmg_res

        # Havoc DMG RES
        stat_bonus_havoc_dmg_res = get_number(
            self._old_row[ResonatorTsvColumnEnum.STAT_BONUS_HAVOC_DMG_RES]
        )
        self._new_row[
            CalculatedResonatorTsvColumnEnum.CALCULATED_HAVOC_DMG_RES.value
        ] = stat_bonus_havoc_dmg_res


class CalculatedResonators:
    def __init__(
        self,
        resonators_table: ResonatorsTable,
        echoes_table: Optional[EchoesTable] = None,
        callback: Callable[[dict], bool] = None,
    ):
        self.resonators_table = resonators_table
        self.echoes_table = echoes_table
        self.callback = callback

        self.init()

    def init(self):
        resonators_df = self.resonators_table.df

        calculated_resonators_columns = [
            e.value for e in CalculatedResonatorTsvColumnEnum
        ]
        calculated_resonators_dict = {
            column: [] for column in calculated_resonators_columns
        }
        calculated_resonator_id_to_name = OrderedDict()

        c = 0
        for _, row in resonators_df.iterrows():
            c += 1
            try:
                new_resonator = CalculatedResonator(row)
                if self.echoes_table is not None:
                    new_resonator.echoes_table = self.echoes_table
                new_resonator.calculate()

                new_resonator_dict = new_resonator.get_row_dict()
                new_resonator_id = new_resonator_dict.get(
                    CalculatedResonatorTsvColumnEnum.ID.value, None
                )
                new_resonator_name = new_resonator_dict.get(
                    CalculatedResonatorTsvColumnEnum.NAME.value, None
                )

                if self.callback is not None:
                    check = self.callback(new_resonator_dict)
                    if not check:
                        continue
                calculated_resonator_id_to_name[new_resonator_id] = new_resonator_name

                if not new_resonator_id:
                    for col in calculated_resonators_columns:
                        calculated_resonators_dict[col].append("")
                else:
                    for col in calculated_resonators_columns:
                        cell = new_resonator_dict.get(col, None)
                        calculated_resonators_dict[col].append(cell)

            except TypeError:
                continue

        self._id_to_name = calculated_resonator_id_to_name
        self._dict = calculated_resonators_dict
        self._df = pd.DataFrame(calculated_resonators_dict)

        self._table = CalculatedResonatorsTable()
        self._table.df = self._df

    def get_ids(self) -> List[str]:
        return list(self._id_to_name.keys())

    def get_id_to_name(self) -> Dict[str, str]:
        return self._id_to_name

    def get_3_ids(self) -> List[str]:
        ids = self.get_ids()
        ids_3 = ["", "", ""]
        length = min(len(ids), len(ids_3))
        for i in range(length):
            ids_3[i] = ids[i]
        return ids_3

    def get_df(self) -> pd.DataFrame:
        return self._df

    def get_table(self) -> CalculatedResonatorsTable:
        return self._table


def get_calculated_resonators_df() -> pd.DataFrame:
    resonators_table = ResonatorsTable()
    return CalculatedResonators(resonators_table).get_df()


def calc():
    df = get_calculated_resonators_df()
    fpath = Path(CALCULATED_RESONATOR_PATH)
    os.makedirs(fpath.parent, exist_ok=True)
    df.to_csv(fpath, sep="\t", index=False)
