import pandas as pd

from ww.model.monsters import MonstersEnum
from ww.model.resonators import CalculatedResonatorsEnum, ResonatorsEnum
from ww.model.template import CalculatedTemplateEnum, TemplateEnum
from ww.tables.monsters import MonstersTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.utils.number import get_number


def get_damage(
    template_id: str, monster_name: str, r_id_1: str, r_id_2: str, r_id_3: str
):
    calculated_resonators_table = CalculatedResonatorsTable()
    resonators_table = ResonatorsTable()

    monsters_table = MonstersTable()
    monsters_def = monsters_table.search(monster_name, MonstersEnum.DEF)

    template_table = TemplateTable(template_id)
    calculated_template_columns = [e.value for e in CalculatedTemplateEnum]
    calculated_template_dict = {column: [] for column in calculated_template_columns}

    resonators_name2id = {}
    r_ids = [r_id_1, r_id_2, r_id_3]
    for r_id in r_ids:
        n = resonators_table.search(r_id, ResonatorsEnum.NAME)
        if n is not None:
            resonators_name2id[n] = r_id

    for _, row in template_table.df.iterrows():
        calculated_template_row_dict = {
            column: None for column in calculated_template_columns
        }

        resonator_name = row[TemplateEnum.RESONATOR_NAME]
        resonator_id = resonators_name2id.get(resonator_name, None)
        if resonator_id is None:
            continue

        # ATK Percentage
        calculated_atk_p = get_number(
            calculated_resonators_table.search(
                resonator_id, CalculatedResonatorsEnum.CALCULATED_ATK_P
            )
        )
        bonus_atk_p = get_number(row[TemplateEnum.BONUS_ATK_P])
        calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ATK_P.value] = (
            calculated_atk_p + bonus_atk_p
        )

        # ATK
        resonator_atk = get_number(
            calculated_resonators_table.search(
                resonator_id, CalculatedResonatorsEnum.ATK
            )
        )
        weapon_atk = get_number(
            calculated_resonators_table.search(
                resonator_id, CalculatedResonatorsEnum.WEAPON_ATK
            )
        )
        calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ATK.value] = (
            resonator_atk + weapon_atk
        )

        # Additional ATK
        calculated_template_row_dict[
            CalculatedTemplateEnum.FINAL_ATK_ADDITION.value
        ] = get_number(row[TemplateEnum.BONUS_ATK])

        # CRIT Rate
        resonator_crit_rate = get_number(
            calculated_resonators_table.search(
                resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_RATE
            )
        )
        bonus_crit_rate = get_number(row[TemplateEnum.BONUS_CRIT_RATE])
        calculated_template_row_dict[CalculatedTemplateEnum.FINAL_CRIT_RATE.value] = (
            resonator_crit_rate + bonus_crit_rate
        )

        # CRIT DMG
        resonator_crit_dmg = get_number(
            calculated_resonators_table.search(
                resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_DMG
            )
        )
        bonus_crit_dmg = get_number(row[TemplateEnum.BONUS_CRIT_DMG])
        calculated_template_row_dict[CalculatedTemplateEnum.FINAL_CRIT_DMG.value] = (
            resonator_crit_dmg + bonus_crit_dmg
        )

        # BONUS

        print(calculated_template_row_dict)
        return
