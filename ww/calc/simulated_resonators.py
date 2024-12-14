from typing import List

import pandas as pd

from ww.calc.calculated_resonators import (
    get_calculated_resonators_df_by_resonators_table,
)
from ww.calc.simulated_echoes import SimulatedEchoes, get_simulated_echo_id
from ww.locale import ZhTwEnum, _
from ww.model.resonator import (
    ResonatorInformationModel,
    ResonatorStatTsvColumnEnum,
    ResonatorTsvColumnEnum,
)
from ww.model.template import TemplateModel
from ww.model.weapon import WeaponStatEnum
from ww.tables.echo import EchoTable
from ww.tables.resonator import (
    CalculatedResonatorsTable,
    ResonatorsTable,
    get_resonator_information,
)
from ww.tables.weapon import WeaponStatTable


def get_df_by_resonators(
    resonators: List[dict], column_names: List[str]
) -> pd.DataFrame:
    data = {name: [] for name in column_names}
    for resonator in resonators:
        for column_name in column_names:
            data[column_name].append(resonator[column_name])

    df = pd.DataFrame(data, columns=column_names)
    return df


class SimulatedResonators:

    def __init__(
        self,
        resonator_name: str,
        template: TemplateModel,
        echo_table: EchoTable = EchoTable,
        weapon_stat_table: WeaponStatTable = WeaponStatTable,
        simulated_echoes: SimulatedEchoes = SimulatedEchoes,
    ):
        self.resonator_name = resonator_name
        self.template = template

        self.echo_table = echo_table()
        self.weapon_stat_table = weapon_stat_table
        self.simulated_echoes = simulated_echoes()

        self.resonators_table_column_names = [e.value for e in ResonatorTsvColumnEnum]

    def get_empty_resonator(
        self, resonator_name: str, chain: str, weapon_name: str, weapon_tune: str
    ) -> dict:
        resonator = {name: "" for name in self.resonators_table_column_names}
        resonator[ResonatorTsvColumnEnum.NAME.value] = resonator_name
        resonator[ResonatorTsvColumnEnum.RESONANCE_CHAIN.value] = chain
        resonator[ResonatorTsvColumnEnum.WEAPON_NAME.value] = weapon_name
        resonator[ResonatorTsvColumnEnum.WEAPON_RANK.value] = weapon_tune

        resonator[ResonatorTsvColumnEnum.LEVEL.value] = "90"
        resonator[ResonatorTsvColumnEnum.WEAPON_LEVEL.value] = "90"

        resonator[ResonatorTsvColumnEnum.MAX_STA.value] = "240"

        resonator[ResonatorTsvColumnEnum.NORMAL_ATTACK_LV.value] = "10"
        resonator[ResonatorTsvColumnEnum.RESONANCE_SKILL_LV.value] = "10"
        resonator[ResonatorTsvColumnEnum.RESONANCE_LIBERATION_LV.value] = "10"
        resonator[ResonatorTsvColumnEnum.FORTE_CIRCUIT_LV.value] = "10"
        resonator[ResonatorTsvColumnEnum.INTRO_SKILL_LV.value] = "10"
        resonator[ResonatorTsvColumnEnum.OUTRO_SKILL_LV.value] = "1"

        resonator[ResonatorTsvColumnEnum.INHERENT_SKILL_1.value] = "1"
        resonator[ResonatorTsvColumnEnum.INHERENT_SKILL_2.value] = "1"

        resonator[ResonatorTsvColumnEnum.STAT_BONUS_PHYSICAL_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_GLACIO_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_FUSION_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_ELECTRO_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_AERO_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_SPECTRO_DMG_RES.value] = "0.00%"
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HAVOC_DMG_RES.value] = "0.00%"

        return resonator

    def is_weapon_crit_rate(self, weapon_name: str) -> bool:
        weapon_level = "90"
        weapon_stat_table: WeaponStatTable = self.weapon_stat_table(weapon_name)
        weapon_crit_rate = weapon_stat_table.search(
            weapon_level, WeaponStatEnum.CRIT_RATE
        )

        if weapon_crit_rate:
            return True
        return False

    def update_resonator_by_resonator_information(
        self, resonator: dict, resonator_information: ResonatorInformationModel
    ):
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HP_P.value] = (
            resonator_information.stat_bonus.hp_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_ATK_P.value] = (
            resonator_information.stat_bonus.atk_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_DEF_P.value] = (
            resonator_information.stat_bonus.def_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_RATE.value] = (
            resonator_information.stat_bonus.crit_rate
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_DMG.value] = (
            resonator_information.stat_bonus.crit_dmg
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_GLACIO_DMG_BONUS.value] = (
            resonator_information.stat_bonus.glacio
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_FUSION_DMG_BONUS.value] = (
            resonator_information.stat_bonus.fusion
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_ELECTRO_DMG_BONUS.value] = (
            resonator_information.stat_bonus.electro
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_AERO_DMG_BONUS.value] = (
            resonator_information.stat_bonus.aero
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_SPECTRO_DMG_BONUS.value] = (
            resonator_information.stat_bonus.spectro
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HAVOC_DMG_BONUS.value] = (
            resonator_information.stat_bonus.havoc
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HEALING_BONUS.value] = (
            resonator_information.stat_bonus.healing
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_SKILL_BONUS.value] = (
            resonator_information.stat_bonus.resonance_skill
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_BASIC_ATTACK_BONUS.value] = (
            resonator_information.stat_bonus.basic_attack
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HEAVY_ATTACK_BONUS.value] = (
            resonator_information.stat_bonus.heavy_attack
        )
        resonator[
            ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_LIBERATION_BONUS.value
        ] = resonator_information.stat_bonus.resonance_liberation

    def get_resonator_with_theory_1(
        self,
        resonator_name: str,
        chain: str,
        weapon_name: str,
        weapon_tune: str,
    ) -> dict:
        prefix = _(ZhTwEnum.ECHOES_THEORY_1)
        resonator = self.get_empty_resonator(
            resonator_name, chain, weapon_name, weapon_tune
        )
        resonator[ResonatorTsvColumnEnum.ID.value] = resonator_name

        resonator_information = get_resonator_information(resonator_name)
        resonator_element = resonator_information.element
        self.update_resonator_by_resonator_information(resonator, resonator_information)

        resonator_sonatas = self.template.get_sonatas(resonator_name)
        if self.is_weapon_crit_rate(weapon_name):
            main_affix_4c = _(ZhTwEnum.ABBR_CRIT_DMG)
        else:
            main_affix_4c = _(ZhTwEnum.ABBR_CRIT_RATE)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        if resonator_base_attr == ResonatorStatTsvColumnEnum.HP.value:
            main_affix_1c = _(ZhTwEnum.ABBR_HP)
        elif resonator_base_attr == ResonatorStatTsvColumnEnum.ATK.value:
            main_affix_1c = _(ZhTwEnum.ABBR_ATK)
        elif resonator_base_attr == ResonatorStatTsvColumnEnum.DEF.value:
            main_affix_1c = _(ZhTwEnum.ABBR_DEF)

        resonator[ResonatorTsvColumnEnum.ECHO_1.value] = get_simulated_echo_id(
            4, prefix, main_affix_4c, resonator_sonatas[0], 1
        )
        resonator[ResonatorTsvColumnEnum.ECHO_2.value] = get_simulated_echo_id(
            3, prefix, resonator_element, resonator_sonatas[1], 1
        )
        resonator[ResonatorTsvColumnEnum.ECHO_3.value] = get_simulated_echo_id(
            3, prefix, resonator_element, resonator_sonatas[2], 2
        )
        resonator[ResonatorTsvColumnEnum.ECHO_4.value] = get_simulated_echo_id(
            1, prefix, main_affix_1c, resonator_sonatas[3], 1
        )
        resonator[ResonatorTsvColumnEnum.ECHO_5.value] = get_simulated_echo_id(
            1, prefix, main_affix_1c, resonator_sonatas[4], 2
        )

        return resonator

    def get_resonator_table_with_theory_1(self) -> ResonatorsTable:
        resonators = []
        for resonator in self.template.resonators:
            resonator_name = resonator.resonator_name
            resonator_chain = resonator.resonator_chain
            weapon_name = resonator.resonator_weapon_name
            weapon_tune = resonator.resonator_weapon_rank

            resonator_dict = self.get_resonator_with_theory_1(
                resonator_name, resonator_chain, weapon_name, weapon_tune
            )
            resonators.append(resonator_dict)

        df = get_df_by_resonators(resonators, self.resonators_table_column_names)
        table = ResonatorsTable()
        table.df = df

        return table

    def get_calculated_resonators_table_with_theory_1(
        self,
    ) -> CalculatedResonatorsTable:
        resonators_table = self.get_resonator_table_with_theory_1()
        echoes_table = self.simulated_echoes.get_theory_1_table()
        df = get_calculated_resonators_df_by_resonators_table(
            resonators_table, echoes_table=echoes_table
        )
        table = CalculatedResonatorsTable()
        table.df = df
        return table
