from decimal import Decimal

import pandas as pd

from ww.model.echo import ResonatorEchoTsvColumnEnum
from ww.model.template import TemplateModel
from ww.tables.echo import EchoesTable, EchoMainAffixesTable, EchoSubAffixesTable
from ww.utils.pd import get_empty_df


class SimulatedResonator:

    def __init__(self, resonator_name: str, template: TemplateModel):
        echo_main_affixes_table = EchoMainAffixesTable()
        echo_sub_affixes_table = EchoSubAffixesTable()

        self.echo_main_affixes = echo_main_affixes_table.get_main_affixes()
        self.echo_sub_affixes = echo_sub_affixes_table.get_sub_affixes()

        self.echoes_table_column_names = [e.value for e in ResonatorEchoTsvColumnEnum]
        self.echoes_table = EchoesTable()
        self.echoes_table.df = get_empty_df(self.echoes_table_column_names)

    def get_empty_echo(self, prefix: str, suffix: str, sonata: str):
        echo = {name: "" for name in self.echoes_table_column_names}
        echo[ResonatorEchoTsvColumnEnum.PREFIX.value] = prefix
        echo[ResonatorEchoTsvColumnEnum.SUFFIX.value] = suffix
        echo[ResonatorEchoTsvColumnEnum.ECHO_SONATA.value] = sonata

    def get_echo_4c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "4"
        echo = self.get_empty_echo(
            prefix, f"{sonata}-{cost}c-{main_affix}-{no}", sonata
        )
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK.value] = (
            self.echo_main_affixes.cost_4.atk
        )
        return echo

    def get_echo_4c_crit_rate(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "暴", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_CRIT_RATE.value] = (
            self.echo_main_affixes.cost_4.crit_rate
        )
        return echo

    def get_echo_4c_crit_dmg(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "暴傷", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_CRIT_DMG.value] = (
            self.echo_main_affixes.cost_4.crit_dmg
        )
        return echo

    def get_echo_4c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "生", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_4.hp_p
        )
        return echo

    def get_echo_4c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "攻", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_4.atk_p
        )
        return echo

    def get_echo_4c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "防", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_4.def_p
        )
        return echo

    def get_echo_4c_healing(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_4c(prefix, "治", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HEALING_BONUS.value] = (
            self.echo_main_affixes.cost_4.healing
        )
        return echo

    def get_echo_3c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "3"
        echo = self.get_empty_echo(
            prefix, f"{sonata}-{cost}c-{main_affix}-{no}", sonata
        )
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK.value] = (
            self.echo_main_affixes.cost_3.atk
        )
        return echo

    def get_echo_3c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, "生", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_3.hp_p
        )
        return echo

    def get_echo_3c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, "攻", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_3.atk_p
        )
        return echo

    def get_echo_3c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, "防", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_3.def_p
        )
        return echo

    def get_echo_3c_elem(self, prefix: str, element: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, element, sonata, no)
        echo[ResonatorEchoTsvColumnEnum.get_main_dmg_bonus(element)] = (
            self.echo_main_affixes.cost_3.glacio
        )
        return echo

    def get_echo_3c_energy_regen(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_3c(prefix, "共效", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ENERGY_REGEN.value] = (
            self.echo_main_affixes.cost_3.energy_regen
        )
        return echo

    def get_echo_1c(self, prefix: str, main_affix: str, sonata: str, no: int):
        cost = "1"
        echo = self.get_empty_echo(
            prefix, f"{sonata}-{cost}c-{main_affix}-{no}", sonata
        )
        echo[ResonatorEchoTsvColumnEnum.COST.value] = cost
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP.value] = (
            self.echo_main_affixes.cost_1.hp
        )
        return echo

    def get_echo_1c_hp_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, "生", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_HP_P.value] = (
            self.echo_main_affixes.cost_1.hp_p
        )
        return echo

    def get_echo_1c_atk_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, "攻", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_ATK_P.value] = (
            self.echo_main_affixes.cost_1.atk_p
        )
        return echo

    def get_echo_1c_def_p(self, prefix: str, sonata: str, no: int):
        echo = self.get_echo_1c(prefix, "防", sonata, no)
        echo[ResonatorEchoTsvColumnEnum.MAIN_DEF_P.value] = (
            self.echo_main_affixes.cost_1.def_p
        )
        return echo

    def get_base_echoes(self, prefix: str, sonata: str):
        echoes = []

        echo_4c_crit_rate_1 = self.get_echo_4c_crit_rate(prefix, sonata, 1)
        echoes.append(echo_4c_crit_rate_1)

        echo_4c_crit_rate_2 = self.get_echo_4c_crit_rate(prefix, sonata, 2)
        echoes.append(echo_4c_crit_rate_2)

        echo_4c_crit_dmg_1 = self.get_echo_4c_crit_dmg(prefix, sonata, 1)
        echoes.append(echo_4c_crit_dmg_1)

        echo_4c_crit_dmg_2 = self.get_echo_4c_crit_dmg(prefix, sonata, 2)
        echoes.append(echo_4c_crit_dmg_2)

        echo_4c_hp_p_1 = self.get_echo_4c_hp_p(prefix, sonata, 1)
        echoes.append(echo_4c_hp_p_1)

        echo_4c_hp_p_2 = self.get_echo_4c_hp_p(prefix, sonata, 2)
        echoes.append(echo_4c_hp_p_2)

        echo_4c_atk_p_1 = self.get_echo_4c_hp_p(prefix, sonata, 1)
        echoes.append(echo_4c_atk_p_1)

        echo_4c_atk_p_2 = self.get_echo_4c_hp_p(prefix, sonata, 2)
        echoes.append(echo_4c_atk_p_2)

        echo_4c_def_p_1 = self.get_echo_4c_def_p(prefix, sonata, 1)
        echoes.append(echo_4c_def_p_1)

        echo_4c_def_p_2 = self.get_echo_4c_def_p(prefix, sonata, 2)
        echoes.append(echo_4c_def_p_2)

        echo_4c_healing_1 = self.get_echo_4c_healing(prefix, sonata, 1)
        echoes.append(echo_4c_healing_1)

        echo_4c_healing_2 = self.get_echo_4c_healing(prefix, sonata, 2)
        echoes.append(echo_4c_healing_2)

        echo_3c_hp_p_1 = self.get_echo_3c_hp_p(prefix, sonata, 1)
        echoes.append(echo_3c_hp_p_1)

        echo_3c_hp_p_2 = self.get_echo_3c_hp_p(prefix, sonata, 2)
        echoes.append(echo_3c_hp_p_2)

        echo_3c_atk_p_1 = self.get_echo_3c_atk_p(prefix, sonata, 1)
        echoes.append(echo_3c_atk_p_1)

        echo_3c_atk_p_2 = self.get_echo_3c_atk_p(prefix, sonata, 2)
        echoes.append(echo_3c_atk_p_2)

        echo_3c_def_p_1 = self.get_echo_3c_def_p(prefix, sonata, 1)
        echoes.append(echo_3c_def_p_1)

        echo_3c_def_p_2 = self.get_echo_3c_def_p(prefix, sonata, 2)
        echoes.append(echo_3c_def_p_2)

        echo_3c_energy_regen_1 = self.get_echo_3c_energy_regen(prefix, sonata, 1)
        echoes.append(echo_3c_energy_regen_1)

        echo_3c_energy_regen_2 = self.get_echo_3c_energy_regen(prefix, sonata, 2)
        echoes.append(echo_3c_energy_regen_2)

        elements = ["冷凝", "熱熔", "導電", "氣動", "衍射", "湮滅"]
        for element in elements:
            for i in range(1, 3):
                echo_3c_elem = self.get_echo_3c_elem(prefix, element, sonata, i)
                echoes.append(echo_3c_elem)

        echo_1c_hp_p_1 = self.get_echo_1c_hp_p(prefix, sonata, 1)
        echoes.append(echo_1c_hp_p_1)

        echo_1c_hp_p_2 = self.get_echo_1c_hp_p(prefix, sonata, 2)
        echoes.append(echo_1c_hp_p_2)

        echo_1c_atk_p_1 = self.get_echo_1c_atk_p(prefix, sonata, 1)
        echoes.append(echo_1c_atk_p_1)

        echo_1c_atk_p_2 = self.get_echo_1c_atk_p(prefix, sonata, 2)
        echoes.append(echo_1c_atk_p_2)

        echo_1c_def_p_1 = self.get_echo_1c_def_p(prefix, sonata, 1)
        echoes.append(echo_1c_def_p_1)

        echo_1c_def_p_2 = self.get_echo_1c_def_p(prefix, sonata, 2)
        echoes.append(echo_1c_def_p_2)

        return echoes

    def get(self):
        pd.DataFrame({"column_name": []})
