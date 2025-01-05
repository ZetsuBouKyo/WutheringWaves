from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import pandas as pd

from ww.calc.calculated_resonators import (
    get_calculated_resonators_table_by_resonators_table,
)
from ww.calc.simulated_echoes import SimulatedEchoes, get_simulated_echo_id
from ww.locale import ZhTwEnum, _
from ww.model.echo import EchoesModelEnum, ResonatorEchoTsvColumnEnum
from ww.model.resonator import (
    ResonatorInformationModel,
    ResonatorStatTsvColumnEnum,
    ResonatorTsvColumnEnum,
)
from ww.model.resonator_skill import ResonatorSkillBonusTypeEnum
from ww.model.template import TemplateModel
from ww.model.weapon import WeaponStatEnum
from ww.tables.echo import EchoTable
from ww.tables.resonator import (
    CalculatedResonatorsTable,
    ResonatorsTable,
    get_resonator_information,
)
from ww.tables.weapon import WeaponStatTable
from ww.utils.number import get_number


def get_df_by_resonators(
    resonators: List[dict], column_names: List[str]
) -> pd.DataFrame:
    data = {name: [] for name in column_names}
    for resonator in resonators:
        for column_name in column_names:
            data[column_name].append(resonator[column_name])

    df = pd.DataFrame(data, columns=column_names)
    return df


def get_resonator_id(
    prefix: str,
    resonator_name: str,
    resonator_chain: str,
    weapon_name: str,
    weapon_tune: str,
    echo_cost_1: str,
    echo_affix_1: str,
    echo_cost_2: str,
    echo_affix_2: str,
    echo_cost_3: str,
    echo_affix_3: str,
    echo_cost_4: str,
    echo_affix_4: str,
    echo_cost_5: str,
    echo_affix_5: str,
) -> str:

    prefix = f"[{prefix}]"
    resonator = f"+{resonator_chain}{resonator_name}"
    weapon = f"+{weapon_tune}{weapon_name}"
    part_1 = f"{resonator}{weapon}"

    echo_1 = f"{echo_cost_1}{echo_affix_1}"
    echo_2 = f"{echo_cost_2}{echo_affix_2}"
    echo_3 = f"{echo_cost_3}{echo_affix_3}"
    echo_4 = f"{echo_cost_4}{echo_affix_4}"
    echo_5 = f"{echo_cost_5}{echo_affix_5}"
    echo = f"{echo_1}{echo_2}{echo_3}{echo_4}{echo_5}"

    ids = [prefix, part_1, echo]
    return " ".join(ids)


def get_resonators_table(resonators: List[dict], columns: List[str]) -> ResonatorsTable:
    df = get_df_by_resonators(resonators, columns)
    table = ResonatorsTable()
    table.df = df

    return table


def get_prefix_by_resonator_skill_bonus(skill_bonus: str) -> Optional[str]:
    if skill_bonus == ResonatorSkillBonusTypeEnum.BASIC.value:
        prefix = EchoesModelEnum.HALF_BUILT_BASIC_ATK.value
    elif skill_bonus == ResonatorSkillBonusTypeEnum.HEAVY.value:
        prefix = EchoesModelEnum.HALF_BUILT_HEAVY_ATK.value
    elif skill_bonus == ResonatorSkillBonusTypeEnum.RESONANCE_SKILL.value:
        prefix = EchoesModelEnum.HALF_BUILT_RESONANCE_SKILL.value
    elif skill_bonus == ResonatorSkillBonusTypeEnum.RESONANCE_LIBERATION.value:
        prefix = EchoesModelEnum.HALF_BUILT_RESONANCE_LIBERATION.value
    else:
        return
    return prefix


def get_base_affix(base_attr: str) -> str:
    affix = _(ZhTwEnum.ABBR_ATK)
    if base_attr == ResonatorStatTsvColumnEnum.HP.value:
        affix = _(ZhTwEnum.ABBR_HP)
    elif base_attr == ResonatorStatTsvColumnEnum.ATK.value:
        affix = _(ZhTwEnum.ABBR_ATK)
    elif base_attr == ResonatorStatTsvColumnEnum.DEF.value:
        affix = _(ZhTwEnum.ABBR_DEF)
    return affix


class SimulatedResonators:

    def __init__(
        self,
        template: TemplateModel,
        echo_table: Optional[EchoTable] = None,
        weapon_stat_table: WeaponStatTable = WeaponStatTable,
        simulated_echoes: Optional[SimulatedEchoes] = None,
    ):
        self.template = template

        if echo_table is None:
            self.echo_table = EchoTable()
        else:
            self.echo_table = echo_table
        self.weapon_stat_table = weapon_stat_table
        if simulated_echoes is None:
            self.simulated_echoes = SimulatedEchoes()
        else:
            self.simulated_echoes = simulated_echoes

        self.echoes = []
        self.echoes_id_to_echo = {}
        self.echo_ids = set()
        self.resonators_table_column_names = [e.value for e in ResonatorTsvColumnEnum]

    def _get_empty_resonator(
        self,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        echo_name_1: str,
    ) -> dict:
        resonator = {name: "" for name in self.resonators_table_column_names}
        resonator[ResonatorTsvColumnEnum.NAME.value] = resonator_name
        resonator[ResonatorTsvColumnEnum.RESONANCE_CHAIN.value] = resonator_chain
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

        resonator[ResonatorTsvColumnEnum.ECHO_1.value] = echo_name_1

        return resonator

    def _is_weapon_crit_rate(self, weapon_name: str) -> bool:
        weapon_level = "90"
        weapon_stat_table: WeaponStatTable = self.weapon_stat_table(weapon_name)
        weapon_crit_rate = weapon_stat_table.search(
            weapon_level, WeaponStatEnum.CRIT_RATE
        )

        if weapon_crit_rate:
            return True
        return False

    def _update_resonator_by_resonator_information(
        self, resonator: dict, resonator_information: ResonatorInformationModel
    ):
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HP_P.value] = get_number(
            resonator_information.stat_bonus.hp_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_ATK_P.value] = get_number(
            resonator_information.stat_bonus.atk_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_DEF_P.value] = get_number(
            resonator_information.stat_bonus.def_p
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_RATE.value] = get_number(
            resonator_information.stat_bonus.crit_rate
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_CRIT_DMG.value] = get_number(
            resonator_information.stat_bonus.crit_dmg
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_GLACIO_DMG_BONUS.value] = (
            get_number(resonator_information.stat_bonus.glacio)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_FUSION_DMG_BONUS.value] = (
            get_number(resonator_information.stat_bonus.fusion)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_ELECTRO_DMG_BONUS.value] = (
            get_number(resonator_information.stat_bonus.electro)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_AERO_DMG_BONUS.value] = get_number(
            resonator_information.stat_bonus.aero
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_SPECTRO_DMG_BONUS.value] = (
            get_number(resonator_information.stat_bonus.spectro)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HAVOC_DMG_BONUS.value] = get_number(
            resonator_information.stat_bonus.havoc
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HEALING_BONUS.value] = get_number(
            resonator_information.stat_bonus.healing
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_SKILL_BONUS.value] = (
            get_number(resonator_information.stat_bonus.resonance_skill)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_BASIC_ATTACK_BONUS.value] = (
            get_number(resonator_information.stat_bonus.basic_attack)
        )
        resonator[ResonatorTsvColumnEnum.STAT_BONUS_HEAVY_ATTACK_BONUS.value] = (
            get_number(resonator_information.stat_bonus.heavy_attack)
        )
        resonator[
            ResonatorTsvColumnEnum.STAT_BONUS_RESONANCE_LIBERATION_BONUS.value
        ] = get_number(resonator_information.stat_bonus.resonance_liberation)

    def _update_resonator_by_echoes(
        self,
        resonator: dict,
        echo_1: dict,
        echo_2: dict,
        echo_3: dict,
        echo_4: dict,
        echo_5: dict,
    ):
        resonator[ResonatorTsvColumnEnum.ECHO_1.value] = echo_1[
            ResonatorEchoTsvColumnEnum.ID.value
        ]
        resonator[ResonatorTsvColumnEnum.ECHO_2.value] = echo_2[
            ResonatorEchoTsvColumnEnum.ID.value
        ]
        resonator[ResonatorTsvColumnEnum.ECHO_3.value] = echo_3[
            ResonatorEchoTsvColumnEnum.ID.value
        ]
        resonator[ResonatorTsvColumnEnum.ECHO_4.value] = echo_4[
            ResonatorEchoTsvColumnEnum.ID.value
        ]
        resonator[ResonatorTsvColumnEnum.ECHO_5.value] = echo_5[
            ResonatorEchoTsvColumnEnum.ID.value
        ]

    def _add_echo(self, echo: dict):
        echo_id = echo[ResonatorEchoTsvColumnEnum.ID.value]
        if echo_id in self.echo_ids:
            return
        self.echo_ids.add(echo_id)
        self.echoes.append(echo)
        self.echoes_id_to_echo[echo_id] = echo

    def _get_resonator_with_43311_3c_2elem(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        resonator_element = resonator_information.element
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, resonator_element, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, resonator_element, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            resonator_element,
            echo_cost_3,
            resonator_element,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_43311_3c_1elem_1attr(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        resonator_element = resonator_information.element
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, resonator_element, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, base_affix, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            resonator_element,
            echo_cost_3,
            base_affix,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_43311_3c_2attr(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, base_affix, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, base_affix, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            base_affix,
            echo_cost_3,
            base_affix,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_43311_3c_2g(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        main_affix_3c = _(ZhTwEnum.ABBR_ENERGY_REGEN)

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, main_affix_3c, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, main_affix_3c, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            main_affix_3c,
            echo_cost_3,
            main_affix_3c,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_43311_3c_1g_1attr(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)

        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        main_affix_3c = _(ZhTwEnum.ABBR_ENERGY_REGEN)

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, main_affix_3c, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, base_affix, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            main_affix_3c,
            echo_cost_3,
            base_affix,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_43311_3c_1g_1elem(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        resonator_element = resonator_information.element
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "3"
        echo_cost_3 = "3"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        main_affix_3c = _(ZhTwEnum.ABBR_ENERGY_REGEN)

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, resonator_element, resonator_sonatas[1], "1"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, main_affix_3c, resonator_sonatas[2], "2"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "1"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "2"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c,
            echo_cost_2,
            resonator_element,
            echo_cost_3,
            main_affix_3c,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator_with_44111(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        main_affix_4c_1: str,
        main_affix_4c_2: str,
        echo_name_1: str,
    ):
        resonator = self._get_empty_resonator(
            resonator_name, resonator_chain, weapon_name, weapon_tune, echo_name_1
        )

        resonator_information = get_resonator_information(resonator_name)
        self._update_resonator_by_resonator_information(
            resonator, resonator_information
        )

        resonator_sonatas = self.template.get_sonatas(resonator_name)

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        echo_cost_1 = "4"
        echo_cost_2 = "4"
        echo_cost_3 = "1"
        echo_cost_4 = "1"
        echo_cost_5 = "1"

        echo_1 = self.simulated_echoes.get_echo(
            echo_cost_1,
            prefix,
            main_affix_4c_1,
            resonator_sonatas[0],
            "1",
            name=echo_name_1,
        )
        echo_2 = self.simulated_echoes.get_echo(
            echo_cost_2, prefix, main_affix_4c_2, resonator_sonatas[1], "2"
        )
        echo_3 = self.simulated_echoes.get_echo(
            echo_cost_3, prefix, base_affix, resonator_sonatas[2], "1"
        )
        echo_4 = self.simulated_echoes.get_echo(
            echo_cost_4, prefix, base_affix, resonator_sonatas[3], "2"
        )
        echo_5 = self.simulated_echoes.get_echo(
            echo_cost_5, prefix, base_affix, resonator_sonatas[4], "3"
        )

        self._update_resonator_by_echoes(
            resonator, echo_1, echo_2, echo_3, echo_4, echo_5
        )

        self._add_echo(echo_1)
        self._add_echo(echo_2)
        self._add_echo(echo_3)
        self._add_echo(echo_4)
        self._add_echo(echo_5)

        resonator[ResonatorTsvColumnEnum.ID.value] = get_resonator_id(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            echo_cost_1,
            main_affix_4c_1,
            echo_cost_2,
            main_affix_4c_2,
            echo_cost_3,
            base_affix,
            echo_cost_4,
            base_affix,
            echo_cost_5,
            base_affix,
        )

        return resonator

    def _get_resonator(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        echo_name_1: str,
    ) -> dict:
        if self._is_weapon_crit_rate(weapon_name):
            main_affix_4c = _(ZhTwEnum.ABBR_CRIT_DMG)
        else:
            main_affix_4c = _(ZhTwEnum.ABBR_CRIT_RATE)

        resonator = self._get_resonator_with_43311_3c_2elem(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            main_affix_4c,
            echo_name_1,
        )
        return resonator

    def _get_resonators(
        self,
        prefix: str,
        resonator_name: str,
        resonator_chain: str,
        weapon_name: str,
        weapon_tune: str,
        echo_name_1: str,
    ) -> List[dict]:
        if not resonator_name:
            return []
        resonators = []

        resonator_base_attr = self.template.get_base_attr(resonator_name)
        base_affix = get_base_affix(resonator_base_attr)

        main_affixes_4c = [
            _(ZhTwEnum.ABBR_CRIT_RATE),
            _(ZhTwEnum.ABBR_CRIT_DMG),
            base_affix,
        ]
        for main_affix_4c in main_affixes_4c:
            resonator_1 = self._get_resonator_with_43311_3c_2elem(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )
            resonator_2 = self._get_resonator_with_43311_3c_1elem_1attr(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )
            resonator_3 = self._get_resonator_with_43311_3c_2attr(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )

            resonator_4 = self._get_resonator_with_43311_3c_2g(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )

            resonator_5 = self._get_resonator_with_43311_3c_1g_1attr(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )

            resonator_6 = self._get_resonator_with_43311_3c_1g_1elem(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                main_affix_4c,
                echo_name_1,
            )

            resonators.append(resonator_1)
            resonators.append(resonator_2)
            resonators.append(resonator_3)
            resonators.append(resonator_4)
            resonators.append(resonator_5)
            resonators.append(resonator_6)

        resonator_sonatas = self.template.get_sonatas(resonator_name)
        has_44111 = self.echo_table.has_44111(resonator_sonatas)
        if has_44111:
            main_affixes_4c = [
                (_(ZhTwEnum.ABBR_CRIT_RATE), _(ZhTwEnum.ABBR_CRIT_RATE)),
                (_(ZhTwEnum.ABBR_CRIT_RATE), _(ZhTwEnum.ABBR_CRIT_DMG)),
                (_(ZhTwEnum.ABBR_CRIT_RATE), base_affix),
                (_(ZhTwEnum.ABBR_CRIT_DMG), _(ZhTwEnum.ABBR_CRIT_DMG)),
                (_(ZhTwEnum.ABBR_CRIT_DMG), base_affix),
                (base_affix, base_affix),
            ]
            for main_affix_4c_1, main_affix_4c_2 in main_affixes_4c:
                resonator = self._get_resonator_with_44111(
                    prefix,
                    resonator_name,
                    resonator_chain,
                    weapon_name,
                    weapon_tune,
                    main_affix_4c_1,
                    main_affix_4c_2,
                    echo_name_1,
                )
                resonators.append(resonator)

        return resonators

    def get_3_resonators_with_prefix(
        self, prefix: str
    ) -> Tuple[Dict[str, str], ResonatorsTable]:
        resonator_name_to_id = OrderedDict()
        resonators = []
        for resonator in self.template.resonators:
            resonator_name = resonator.resonator_name
            resonator_chain = resonator.resonator_chain
            resonator_echo_1 = resonator.resonator_echo_1
            weapon_name = resonator.resonator_weapon_name
            weapon_tune = resonator.resonator_weapon_rank

            if not resonator_name or not weapon_name or not weapon_tune:
                continue

            # Table
            resonator_dict = self._get_resonator(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                resonator_echo_1,
            )
            resonators.append(resonator_dict)

            # Resonator ID
            resonator_id = resonator_dict[ResonatorTsvColumnEnum.ID.value]
            resonator_name_to_id[resonator_name] = resonator_id

        table = get_resonators_table(resonators, self.resonators_table_column_names)
        return resonator_name_to_id, table

    def get_3_resonators_with_half_built_skill_bonus(
        self,
    ) -> Tuple[Dict[str, str], ResonatorsTable]:
        resonator_name_to_id = OrderedDict()
        resonators = []
        for resonator in self.template.resonators:
            resonator_name = resonator.resonator_name
            resonator_chain = resonator.resonator_chain
            resonator_echo_1 = resonator.resonator_echo_1
            weapon_name = resonator.resonator_weapon_name
            weapon_tune = resonator.resonator_weapon_rank

            if not resonator_name:
                continue

            prefix = get_prefix_by_resonator_skill_bonus(
                resonator.resonator_skill_bonus
            )
            if prefix is None:
                continue

            resonator_dict = self._get_resonator(
                prefix,
                resonator_name,
                resonator_chain,
                weapon_name,
                weapon_tune,
                resonator_echo_1,
            )
            resonators.append(resonator_dict)

            # Resonator ID
            resonator_id = resonator_dict[ResonatorTsvColumnEnum.ID.value]
            resonator_name_to_id[resonator_name] = resonator_id

        table = get_resonators_table(resonators, self.resonators_table_column_names)
        return resonator_name_to_id, table

    def get_resonators_for_echo_comparison_with_prefix(
        self, resonator_name: str, prefix: str
    ) -> Tuple[List[str], ResonatorsTable]:
        resonator = self.template.get_resonator(resonator_name)
        resonator_name = resonator.resonator_name
        resonator_chain = resonator.resonator_chain
        resonator_echo_1 = resonator.resonator_echo_1
        weapon_name = resonator.resonator_weapon_name
        weapon_tune = resonator.resonator_weapon_rank

        resonators = self._get_resonators(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            resonator_echo_1,
        )

        resonator_ids = []
        for r in resonators:
            resonator_ids.append(r[ResonatorTsvColumnEnum.ID.value])

        table = get_resonators_table(resonators, self.resonators_table_column_names)
        return resonator_ids, table

    def get_resonators_for_echo_comparison_with_half_built_skill_bonus(
        self, resonator_name: str
    ) -> Tuple[List[str], ResonatorsTable]:
        resonator = self.template.get_resonator(resonator_name)
        resonator_name = resonator.resonator_name
        resonator_chain = resonator.resonator_chain
        resonator_skill_bonus = resonator.resonator_skill_bonus
        resonator_echo_1 = resonator.resonator_echo_1

        weapon_name = resonator.resonator_weapon_name
        weapon_tune = resonator.resonator_weapon_rank

        prefix = get_prefix_by_resonator_skill_bonus(resonator_skill_bonus)

        resonators = self._get_resonators(
            prefix,
            resonator_name,
            resonator_chain,
            weapon_name,
            weapon_tune,
            resonator_echo_1,
        )

        resonator_ids = []
        for r in resonators:
            resonator_ids.append(r[ResonatorTsvColumnEnum.ID.value])

        table = get_resonators_table(resonators, self.resonators_table_column_names)
        return resonator_ids, table

    def get_calculated_resonators_table(
        self, resonators_table: ResonatorsTable
    ) -> CalculatedResonatorsTable:
        echoes_table = self.simulated_echoes.get_simulated_table_with_echoes(
            self.echoes_id_to_echo
        )
        table = get_calculated_resonators_table_by_resonators_table(
            resonators_table, echoes_table=echoes_table
        )

        return table
