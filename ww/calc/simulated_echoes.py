from decimal import Decimal
from statistics import mean
from typing import List, Optional

import pandas as pd

from ww.locale import ZhTwEnum, _
from ww.model.echo import (
    EchoesModelEnum,
    EchoSonataEnum,
    ResonatorEchoTsvColumnEnum,
    get_resonator_echo_main_dmg_bonus,
)
from ww.model.element import ElementEnum
from ww.tables.echo import EchoesTable, EchoMainAffixesTable, EchoSubAffixesTable
from ww.utils.pd import get_empty_df

ECHOES_THEORY_1_FPATH = "./data/v1/zh_tw/echoes_theory_1.tsv"


def get_simulated_echo_id(
    cost: str, prefix: str, main_affix: str, sonata: str, no: str
) -> str:
    return f"{prefix} {sonata} {cost}c {main_affix} {no}"


class SimulatedEchoes:

    def __init__(self, echoes_theory_1_fpath: str = ECHOES_THEORY_1_FPATH):
        self.echoes_theory_1_fpath = echoes_theory_1_fpath

        echo_main_affixes_table = EchoMainAffixesTable()
        echo_sub_affixes_table = EchoSubAffixesTable()

        self.echo_main_affixes = echo_main_affixes_table.get_main_affixes()
        self.echo_sub_affixes = echo_sub_affixes_table.get_sub_affixes()

        self.echoes_table_column_names = [e.value for e in ResonatorEchoTsvColumnEnum]
        self.echoes_table = EchoesTable()
        self.echoes_table.df = get_empty_df(self.echoes_table_column_names)

    def get_empty_echo(
        self, cost: int, prefix: str, main_affix: str, sonata: str, no: int
    ):
        echo = {name: "" for name in self.echoes_table_column_names}
        echo[ResonatorEchoTsvColumnEnum.ID.value] = get_simulated_echo_id(
            cost, prefix, main_affix, sonata, no
        )
        echo[ResonatorEchoTsvColumnEnum.ECHO_SONATA.value] = sonata
        return echo

    def get_echo_4c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "4"
        echo = self.get_empty_echo(cost, prefix, main_affix, sonata, no)
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK.value] = (
            self.echo_main_affixes.cost_4.atk
        )
        return echo

    def get_echo_4c_crit_rate(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_CRIT_RATE), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_CRIT_RATE.value] = (
            self.echo_main_affixes.cost_4.crit_rate
        )
        return echo

    def get_echo_4c_crit_dmg(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_CRIT_DMG), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_CRIT_DMG.value] = (
            self.echo_main_affixes.cost_4.crit_dmg
        )
        return echo

    def get_echo_4c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_HP), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_4.hp_p
        )
        return echo

    def get_echo_4c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_ATK), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_4.atk_p
        )
        return echo

    def get_echo_4c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_DEF), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_4.def_p
        )
        return echo

    def get_echo_4c_healing(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, _(ZhTwEnum.ABBR_HEALING), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HEALING_BONUS.value] = (
            self.echo_main_affixes.cost_4.healing
        )
        return echo

    def get_echo_3c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "3"
        echo = self.get_empty_echo(cost, prefix, main_affix, sonata, no)
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK.value] = (
            self.echo_main_affixes.cost_3.atk
        )
        return echo

    def get_echo_3c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, _(ZhTwEnum.ABBR_HP), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_3.hp_p
        )
        return echo

    def get_echo_3c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, _(ZhTwEnum.ABBR_ATK), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_3.atk_p
        )
        return echo

    def get_echo_3c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, _(ZhTwEnum.ABBR_DEF), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_3.def_p
        )
        return echo

    def get_echo_3c_elem(self, prefix: str, element: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, element, sonata, no)
        echo[get_resonator_echo_main_dmg_bonus(element)] = (
            self.echo_main_affixes.cost_3.glacio
        )
        return echo

    def get_echo_3c_energy_regen(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, _(ZhTwEnum.ABBR_ENERGY_REGEN), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ENERGY_REGEN.value] = (
            self.echo_main_affixes.cost_3.energy_regen
        )
        return echo

    def get_echo_1c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "1"
        echo = self.get_empty_echo(cost, prefix, main_affix, sonata, no)
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP.value] = (
            self.echo_main_affixes.cost_1.hp
        )
        return echo

    def get_echo_1c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, _(ZhTwEnum.ABBR_HP), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_1.hp_p
        )
        return echo

    def get_echo_1c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, _(ZhTwEnum.ABBR_ATK), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_1.atk_p
        )
        return echo

    def get_echo_1c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, _(ZhTwEnum.ABBR_DEF), sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_1.def_p
        )
        return echo

    def get_base_echoes(self, prefix: str, sonata: str):
        echoes = []

        for get_echo_4c in [
            self.get_echo_4c_crit_rate,
            self.get_echo_4c_crit_dmg,
            self.get_echo_4c_hp_p,
            self.get_echo_4c_atk_p,
            self.get_echo_4c_def_p,
            self.get_echo_4c_healing,
        ]:
            for i in range(1, 3):
                echo_4c = get_echo_4c(prefix, sonata, i)
                echoes.append(echo_4c)

        for get_echo_3c in [
            self.get_echo_3c_hp_p,
            self.get_echo_3c_atk_p,
            self.get_echo_3c_def_p,
            self.get_echo_3c_energy_regen,
        ]:
            for i in range(1, 3):
                echo_3c = get_echo_3c(prefix, sonata, i)
                echoes.append(echo_3c)

        elements = [
            _(ZhTwEnum.GLACIO),
            _(ZhTwEnum.FUSION),
            _(ZhTwEnum.ELECTRO),
            _(ZhTwEnum.AERO),
            _(ZhTwEnum.SPECTRO),
            _(ZhTwEnum.HAVOC),
        ]
        for element in elements:
            for i in range(1, 3):
                echo_3c_elem = self.get_echo_3c_elem(prefix, element, sonata, i)
                echoes.append(echo_3c_elem)

        for get_echo_1c in [
            self.get_echo_1c_hp_p,
            self.get_echo_1c_atk_p,
            self.get_echo_1c_def_p,
        ]:
            for i in range(1, 4):
                echo_1c = get_echo_1c(prefix, sonata, i)
                echoes.append(echo_1c)

        return echoes

    def update_echo_sub_affix_with_theory_1(self, echo: dict):
        echo[ResonatorEchoTsvColumnEnum.SUB_ATK.value] = Decimal("24")
        echo[ResonatorEchoTsvColumnEnum.SUB_ATK_P.value] = Decimal("0.054")
        echo[ResonatorEchoTsvColumnEnum.SUB_CRIT_RATE.value] = Decimal("0.084")
        echo[ResonatorEchoTsvColumnEnum.SUB_CRIT_DMG.value] = Decimal("0.1008")
        echo[ResonatorEchoTsvColumnEnum.SUB_ENERGY_REGEN.value] = Decimal("0.0192")

        echo[ResonatorEchoTsvColumnEnum.SUB_RESONANCE_SKILL_DMG_BONUS.value] = Decimal(
            "0.016"
        )
        echo[ResonatorEchoTsvColumnEnum.SUB_BASIC_ATTACK_DMG_BONUS.value] = Decimal(
            "0.016"
        )
        echo[ResonatorEchoTsvColumnEnum.SUB_HEAVY_ATTACK_DMG_BONUS.value] = Decimal(
            "0.016"
        )
        echo[ResonatorEchoTsvColumnEnum.SUB_RESONANCE_LIBERATION_DMG_BONUS.value] = (
            Decimal("0.016")
        )

    def update_echoes_with_theory_1(self, echoes: List[dict], sonata: str):
        prefix = EchoesModelEnum.THEORY_1.value
        echoes = self.get_base_echoes(prefix, sonata)
        for echo in echoes:
            self.update_echo_sub_affix_with_theory_1(echo)

            echoes.append(echo)

    def update_echo_sub_affix_with_half_built(self, echo: dict, prefix: str):
        echo[ResonatorEchoTsvColumnEnum.SUB_CRIT_RATE.value] = mean(
            self.echo_sub_affixes.crit_rate
        )
        echo[ResonatorEchoTsvColumnEnum.SUB_CRIT_DMG.value] = mean(
            self.echo_sub_affixes.crit_dmg
        )
        echo[ResonatorEchoTsvColumnEnum.SUB_ATK_P.value] = mean(
            self.echo_sub_affixes.atk_p
        )

        if prefix == EchoesModelEnum.HALF_BUILT_ATK.value:
            echo[ResonatorEchoTsvColumnEnum.SUB_ATK.value] = mean(
                self.echo_sub_affixes.atk
            )
        elif prefix == EchoesModelEnum.HALF_BUILT_BASIC_ATK.value:
            echo[ResonatorEchoTsvColumnEnum.SUB_BASIC_ATTACK_DMG_BONUS.value] = mean(
                self.echo_sub_affixes.basic_attack
            )
        elif prefix == EchoesModelEnum.HALF_BUILT_BASIC_ATK.value:
            echo[ResonatorEchoTsvColumnEnum.SUB_BASIC_ATTACK_DMG_BONUS.value] = mean(
                self.echo_sub_affixes.basic_attack
            )
        elif prefix == EchoesModelEnum.HALF_BUILT_HEAVY_ATK.value:
            echo[ResonatorEchoTsvColumnEnum.SUB_HEAVY_ATTACK_DMG_BONUS.value] = mean(
                self.echo_sub_affixes.heavy_attack
            )
        elif prefix == EchoesModelEnum.HALF_BUILT_RESONANCE_SKILL.value:
            echo[ResonatorEchoTsvColumnEnum.SUB_RESONANCE_SKILL_DMG_BONUS.value] = mean(
                self.echo_sub_affixes.resonance_skill
            )
        elif prefix == EchoesModelEnum.HALF_BUILT_RESONANCE_LIBERATION.value:
            echo[
                ResonatorEchoTsvColumnEnum.SUB_RESONANCE_LIBERATION_DMG_BONUS.value
            ] = mean(self.echo_sub_affixes.resonance_liberation)

    def update_echoes_with_half_built(
        self, echoes: List[str], prefix: str, sonata: str
    ):
        base_echoes = self.get_base_echoes(prefix, sonata)
        for echo in base_echoes:
            self.update_echo_sub_affix_with_half_built(echo, prefix)

            echoes.append(echo)

    def get_echoes_with_sonatas(self) -> List[str]:
        echoes = []

        for sonata_enum in EchoSonataEnum:
            sonata = sonata_enum.value
            self.update_echoes_with_theory_1(echoes, sonata)

        half_built_prefixes = [
            EchoesModelEnum.HALF_BUILT_ATK.value,
            EchoesModelEnum.HALF_BUILT_BASIC_ATK.value,
            EchoesModelEnum.HALF_BUILT_HEAVY_ATK.value,
            EchoesModelEnum.HALF_BUILT_RESONANCE_SKILL.value,
            EchoesModelEnum.HALF_BUILT_RESONANCE_LIBERATION.value,
        ]
        for prefix in half_built_prefixes:
            for sonata_enum in EchoSonataEnum:
                sonata = sonata_enum.value
                self.update_echoes_with_half_built(echoes, prefix, sonata)

        return echoes

    def get_df(self) -> pd.DataFrame:
        echoes = self.get_echoes_with_sonatas()

        data = {name: [] for name in self.echoes_table_column_names}
        for echo in echoes:
            for key, value in echo.items():
                data[key].append(value)

        df = pd.DataFrame(data, columns=self.echoes_table_column_names)
        return df

    def get_table(self) -> EchoesTable:
        df = self.get_df()
        table = EchoesTable()
        table.df = df
        return table

    def get_table_with_echoes(self, echoes: List[str]) -> EchoesTable:
        data = {name: [] for name in self.echoes_table_column_names}
        for echo in echoes:
            for key, value in echo.items():
                data[key].append(value)

        df = pd.DataFrame(data, columns=self.echoes_table_column_names)
        table = EchoesTable()
        table.df = df
        return table

    def get_echo_with_main_affix(
        self, cost: str, prefix: str, main_affix: str, sonata: str, no: str
    ) -> Optional[dict]:
        echo = None
        elements = [
            ElementEnum.GLACIO.value,
            ElementEnum.FUSION.value,
            ElementEnum.ELECTRO.value,
            ElementEnum.AERO.value,
            ElementEnum.SPECTRO.value,
            ElementEnum.HAVOC.value,
        ]
        if cost == "4":
            if main_affix == _(ZhTwEnum.ABBR_HP):
                echo = self.get_echo_4c_hp_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_ATK):
                echo = self.get_echo_4c_atk_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_DEF):
                echo = self.get_echo_4c_def_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_CRIT_RATE):
                echo = self.get_echo_4c_crit_rate(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_CRIT_DMG):
                echo = self.get_echo_4c_crit_dmg(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_HEALING):
                echo = self.get_echo_4c_healing(prefix, sonata, no)
        elif cost == "3":
            if main_affix == _(ZhTwEnum.ABBR_HP):
                echo = self.get_echo_3c_hp_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_ATK):
                echo = self.get_echo_3c_atk_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_DEF):
                echo = self.get_echo_3c_def_p(prefix, sonata, no)
            elif main_affix in elements:
                echo = self.get_echo_3c_elem(prefix, main_affix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_ENERGY_REGEN):
                echo = self.get_echo_3c_energy_regen(prefix, sonata, no)
        elif cost == "1":
            if main_affix == _(ZhTwEnum.ABBR_HP):
                echo = self.get_echo_1c_hp_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_ATK):
                echo = self.get_echo_1c_atk_p(prefix, sonata, no)
            elif main_affix == _(ZhTwEnum.ABBR_DEF):
                echo = self.get_echo_1c_def_p(prefix, sonata, no)

        return echo

    def get_echo(
        self, cost: str, prefix: str, main_affix: str, sonata: str, no: str
    ) -> Optional[dict]:
        echo = self.get_echo_with_main_affix(cost, prefix, main_affix, sonata, no)
        if echo is None:
            return echo

        half_built_prefixes = [
            EchoesModelEnum.HALF_BUILT_ATK.value,
            EchoesModelEnum.HALF_BUILT_BASIC_ATK.value,
            EchoesModelEnum.HALF_BUILT_HEAVY_ATK.value,
            EchoesModelEnum.HALF_BUILT_RESONANCE_SKILL.value,
            EchoesModelEnum.HALF_BUILT_RESONANCE_LIBERATION.value,
        ]
        if prefix == EchoesModelEnum.THEORY_1.value:
            self.update_echo_sub_affix_with_theory_1(echo)
        elif prefix in half_built_prefixes:
            self.update_echo_sub_affix_with_half_built(echo, prefix)

        return echo