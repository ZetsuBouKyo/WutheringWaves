from decimal import Decimal
from typing import Dict, Optional, Union

import pandas as pd

from ww.model.echo_skill import EchoSkillEnum
from ww.model.monsters import MonstersEnum
from ww.model.resonator_skill import (
    ResonatorSkillBaseAttrEnum,
    ResonatorSkillBonusTypeEnum,
    ResonatorSkillEnum,
)
from ww.model.resonators import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorsEnum,
    ResonatorsEnum,
)
from ww.model.template import CalculatedTemplateEnum, TemplateEnum
from ww.tables.echo_skill import EchoSkillTable
from ww.tables.monsters import MonstersTable
from ww.tables.resonator_skill import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.utils.number import get_number, get_string


def get_row_damage(
    row: pd.DataFrame,
    resonator_id,
    resonator_name,
    monster_name,
    monster_level,
    monster_def,
    resonators_table: ResonatorsTable,
    calculated_resonators_table: CalculatedResonatorsTable,
    echo_skill_table,
    monsters_table: MonstersTable,
    calculated_template_columns,
) -> Optional[Dict[CalculatedTemplateEnum, Union[str, Decimal]]]:
    if resonator_id is None:
        return

    calculated_template_row_dict = {
        column: None for column in calculated_template_columns
    }

    calculated_template_row_dict[CalculatedTemplateEnum.RESONATOR_NAME.value] = (
        resonator_name
    )

    manual_bonus_type = get_string(row[TemplateEnum.BONUS_TYPE])

    resonator_level = get_number(
        resonators_table.search(resonator_id, ResonatorsEnum.LEVEL)
    )

    # Skill
    template_row_skill_id = row[TemplateEnum.SKILL_ID]

    # Resonator Skill Level
    resonator_skills = [
        ResonatorsEnum.NORMAL_ATTACK_LV,
        ResonatorsEnum.RESONANCE_SKILL_LV,
        ResonatorsEnum.RESONANCE_LIBERATION_LV,
        ResonatorsEnum.FORTE_CIRCUIT_LV,
        ResonatorsEnum.INTRO_SKILL_LV,
        ResonatorsEnum.OUTRO_SKILL_LV,
    ]
    resonator_skill_levels = {}
    for s in resonator_skills:
        lv = resonators_table.search(resonator_id, s.value)
        resonator_skill_levels[s.value] = str(lv)

    # Resonator Skill
    resonator_skill_table = ResonatorSkillTable(resonator_name)

    resonator_skill_element = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.SKILL_ELEMENT
    )
    resonator_skill_base_attr = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.SKILL_BASE_ATTR
    )
    resonator_skill_type = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.SKILL_TYPE
    )
    resonator_skill_bonus_type = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.SKILL_TYPE_BONUS
    )
    resonator_skill_lv = resonator_skill_levels.get(f"{resonator_skill_type}LV", None)
    resonator_skill_dmg = resonator_skill_table.search(
        template_row_skill_id, f"LV{resonator_skill_lv}"
    )
    if resonator_skill_dmg is not None:
        resonator_skill_dmg = get_number(resonator_skill_dmg)

    calculated_template_row_dict[CalculatedTemplateEnum.SKILL_ID.value] = (
        template_row_skill_id
    )
    calculated_template_row_dict[CalculatedTemplateEnum.RESONATOR_SKILL_LEVEL.value] = (
        resonator_skill_lv
    )
    calculated_template_row_dict[
        CalculatedTemplateEnum.RESONATOR_SKILL_ELEMENT.value
    ] = resonator_skill_element
    calculated_template_row_dict[
        CalculatedTemplateEnum.RESONATOR_SKILL_BASE_ATTR.value
    ] = resonator_skill_base_attr
    calculated_template_row_dict[CalculatedTemplateEnum.RESONATOR_SKILL_TYPE.value] = (
        resonator_skill_type
    )
    calculated_template_row_dict[
        CalculatedTemplateEnum.RESONATOR_SKILL_TYPE_BONUS.value
    ] = resonator_skill_bonus_type
    calculated_template_row_dict[CalculatedTemplateEnum.RESONATOR_SKILL_DMG.value] = (
        resonator_skill_dmg
    )

    # Echo Skill
    echo_skill_element = echo_skill_table.search(
        template_row_skill_id, EchoSkillEnum.SKILL_ELEMENT
    )
    echo_skill_dmg = echo_skill_table.search(
        template_row_skill_id, EchoSkillEnum.SKILL_DMG
    )
    if echo_skill_dmg is not None:
        echo_skill_dmg = get_number(echo_skill_dmg)

    calculated_template_row_dict[CalculatedTemplateEnum.ECHO_ELEMENT.value] = (
        echo_skill_element
    )
    calculated_template_row_dict[CalculatedTemplateEnum.ECHO_SKILL_DMG.value] = (
        echo_skill_dmg
    )

    # Element
    if not ((resonator_skill_element is None) ^ (echo_skill_element is None)):
        # TODO: raise error
        # print("element")
        return

    if resonator_skill_element is None:
        element = echo_skill_element
    else:
        element = resonator_skill_element
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ELEMENT.value] = element

    # Skill DMG
    if not ((resonator_skill_dmg is None) ^ (echo_skill_dmg is None)):
        # TODO: raise error
        # print("skill dmg")
        return

    if resonator_skill_dmg is None:
        skill_dmg = echo_skill_dmg
        resonator_skill_base_attr = ResonatorSkillBaseAttrEnum.ATK.value
    else:
        skill_dmg = resonator_skill_dmg
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_SKILL_DMG.value] = (
        skill_dmg
    )

    # Bonus Type
    if not (
        (resonator_skill_bonus_type is None)
        ^ (echo_skill_element is None or echo_skill_dmg is None)
    ):
        # TODO: raise error
        # print("bonus type")
        return

    if manual_bonus_type:
        bonus_type = manual_bonus_type
    elif resonator_skill_bonus_type is None:
        bonus_type = ResonatorSkillBonusTypeEnum.ECHO.value
    else:
        bonus_type = resonator_skill_bonus_type
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_BONUS_TYPE.value] = (
        bonus_type
    )

    # Monster
    monster_res = get_number(monsters_table.search(monster_name, f"{element}抗性"))
    calculated_template_row_dict[CalculatedTemplateEnum.MONSTER_LEVEL.value] = (
        monster_level
    )
    calculated_template_row_dict[CalculatedTemplateEnum.MONSTER_DEF.value] = monster_def
    calculated_template_row_dict[CalculatedTemplateEnum.MONSTER_RES.value] = monster_res

    # ATK Percentage
    calculated_atk_p = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_ATK_P
        )
    )
    bonus_atk_p = get_number(row[TemplateEnum.BONUS_ATK_P])
    final_atk_p = calculated_atk_p + bonus_atk_p
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ATK_P.value] = final_atk_p

    # ATK
    resonator_atk = get_number(
        calculated_resonators_table.search(resonator_id, CalculatedResonatorsEnum.ATK)
    )
    weapon_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.WEAPON_ATK
        )
    )
    final_atk = resonator_atk + weapon_atk
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ATK.value] = final_atk

    # Additional ATK
    echo_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.ECHO_ATK
        )
    )
    template_bonus_atk = get_number(row[TemplateEnum.BONUS_ATK])
    final_atk_addition = echo_atk + template_bonus_atk
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_ATK_ADDITION.value] = (
        final_atk_addition
    )

    # CRIT Rate
    resonator_crit_rate = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_RATE
        )
    )
    bonus_crit_rate = get_number(row[TemplateEnum.BONUS_CRIT_RATE])
    final_crit_rate = resonator_crit_rate + bonus_crit_rate
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_CRIT_RATE.value] = (
        final_crit_rate
    )

    # CRIT DMG
    resonator_crit_dmg = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_DMG
        )
    )
    bonus_crit_dmg = get_number(row[TemplateEnum.BONUS_CRIT_DMG])
    final_crit_dmg = resonator_crit_dmg + bonus_crit_dmg
    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_CRIT_DMG.value] = (
        final_crit_dmg
    )

    # BONUS
    calculated_element_bonus_key_name = f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{element}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}"
    calculated_element_bonus = get_number(
        calculated_resonators_table.search(
            resonator_id, calculated_element_bonus_key_name
        )
    )

    calculated_skill_bonus_key_name = f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{bonus_type}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}"
    calculated_skill_bonus = get_number(
        calculated_resonators_table.search(
            resonator_id, calculated_skill_bonus_key_name
        )
    )

    template_bonus = get_number(row[TemplateEnum.BONUS_ADDITION])
    final_bonus = calculated_element_bonus + calculated_skill_bonus + template_bonus

    calculated_template_row_dict[CalculatedTemplateEnum.FINAL_BONUS.value] = final_bonus

    # Other Bonus
    bonus_magnifier = get_number(row[TemplateEnum.BONUS_MAGNIFIER])
    bonus_amplifier = get_number(row[TemplateEnum.BONUS_AMPLIFIER])
    bonus_skill_dmg_addition = get_number(row[TemplateEnum.BONUS_SKILL_DMG_ADDITION])
    bonus_ignore_def = get_number(row[TemplateEnum.BONUS_IGNORE_DEF])
    bonus_reduce_res = get_number(row[TemplateEnum.BONUS_REDUCE_RES])

    # DMG
    if resonator_skill_base_attr == ResonatorSkillBaseAttrEnum.ATK.value:
        region_base_attr = (
            final_atk * (get_number("1.0") + final_atk_p) + final_atk_addition
        )
    else:
        return

    region_skill_dmg = skill_dmg + bonus_skill_dmg_addition
    region_bonus_magnifier = get_number("1.0") + bonus_magnifier
    region_bonus_amplifier = get_number("1.0") + bonus_amplifier
    region_bonus = get_number("1.0") + final_bonus
    region_def = (get_number("800.0") + get_number("8.0") * resonator_level) / (
        get_number("800.0")
        + get_number("8.0") * resonator_level
        + monster_def * (1 - bonus_ignore_def)
    )
    region_bonus_reduce_res = get_number("1.0") + bonus_reduce_res - monster_res
    region_crit_dmg = final_crit_dmg
    region_crit = final_crit_dmg * final_crit_rate + get_number("1.0") - final_crit_rate

    dmg_no_crit = (
        region_base_attr
        * region_skill_dmg
        * region_bonus_magnifier
        * region_bonus_amplifier
        * region_bonus
        * region_def
        * region_bonus_reduce_res
    )
    # print(
    #     region_base_attr,
    #     region_skill_dmg,
    #     region_bonus_magnifier,
    #     region_bonus_amplifier,
    #     region_bonus,
    #     region_def,
    #     region_bonus_reduce_res,
    # )

    dmg_crit = dmg_no_crit * region_crit_dmg
    dmg_avg = dmg_no_crit * region_crit

    calculated_template_row_dict[CalculatedTemplateEnum.DAMAGE.value] = int(dmg_avg)
    calculated_template_row_dict[CalculatedTemplateEnum.DAMAGE_NO_CRIT.value] = int(
        dmg_no_crit
    )
    calculated_template_row_dict[CalculatedTemplateEnum.DAMAGE_CRIT.value] = int(
        dmg_crit
    )

    return calculated_template_row_dict


def get_damage(
    template_id: str, monster_name: str, r_id_1: str, r_id_2: str, r_id_3: str
):
    calculated_resonators_table = CalculatedResonatorsTable()
    resonators_table = ResonatorsTable()

    monsters_table = MonstersTable()
    monster_level = get_number(monsters_table.search(monster_name, MonstersEnum.LEVEL))
    monster_def = get_number(monsters_table.search(monster_name, MonstersEnum.DEF))

    template_table = TemplateTable(template_id)
    calculated_template_columns = [e.value for e in CalculatedTemplateEnum]
    calculated_template_dict = {column: [] for column in calculated_template_columns}

    echo_skill_table = EchoSkillTable()

    resonators_name2id = {}
    r_ids = [r_id_1, r_id_2, r_id_3]
    for r_id in r_ids:
        n = get_string(resonators_table.search(r_id, ResonatorsEnum.NAME))
        if n:
            resonators_name2id[n] = r_id

    results = []
    for _, row in template_table.df.iterrows():
        resonator_name = row[TemplateEnum.RESONATOR_NAME]
        resonator_id = resonators_name2id.get(resonator_name, None)
        if resonator_id is None:
            continue
        calculated_template_row_dict = get_row_damage(
            row,
            resonator_id,
            resonator_name,
            monster_name,
            monster_level,
            monster_def,
            resonators_table,
            calculated_resonators_table,
            echo_skill_table,
            monsters_table,
            calculated_template_columns,
        )
        if calculated_template_row_dict is not None:
            results.append(calculated_template_row_dict)
    return results