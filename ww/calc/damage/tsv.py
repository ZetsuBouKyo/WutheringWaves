from decimal import Decimal
from typing import Dict, Optional, Union

import pandas as pd

from ww.model.buff import SkillBonusTypeEnum
from ww.model.echo import EchoSkillEnum
from ww.model.monsters import MonstersEnum
from ww.model.resonator import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorColumnEnum,
    ResonatorColumnEnum,
)
from ww.model.resonator_skill import ResonatorSkillBaseAttrEnum, ResonatorSkillEnum
from ww.model.template import CalculatedTemplateEnum, TemplateEnum
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersTable
from ww.tables.resonator import (
    CalculatedResonatorsTable,
    ResonatorSkillTable,
    ResonatorsTable,
)
from ww.tables.template import TemplateTable
from ww.utils.number import get_number, get_string


def get_tsv_row_damage(
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
        resonators_table.search(resonator_id, ResonatorColumnEnum.LEVEL)
    )

    # Skill
    template_row_skill_id = row[TemplateEnum.SKILL_ID]

    # Resonator Skill Level
    resonator_skills = [
        ResonatorColumnEnum.NORMAL_ATTACK_LV,
        ResonatorColumnEnum.RESONANCE_SKILL_LV,
        ResonatorColumnEnum.RESONANCE_LIBERATION_LV,
        ResonatorColumnEnum.FORTE_CIRCUIT_LV,
        ResonatorColumnEnum.INTRO_SKILL_LV,
        ResonatorColumnEnum.OUTRO_SKILL_LV,
    ]
    resonator_skill_levels = {}
    for s in resonator_skills:
        lv = resonators_table.search(resonator_id, s.value)
        resonator_skill_levels[s.value] = str(lv)

    # Resonator Skill
    resonator_skill_table = ResonatorSkillTable(resonator_name)

    resonator_skill_element = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.ELEMENT
    )
    resonator_skill_base_attr = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.BASE_ATTR
    )
    resonator_skill_type = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.TYPE_ZH_TW
    )
    resonator_skill_bonus_type = resonator_skill_table.search(
        template_row_skill_id, ResonatorSkillEnum.TYPE_BONUS
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
        template_row_skill_id, EchoSkillEnum.ELEMENT
    )
    echo_skill_dmg = echo_skill_table.search(template_row_skill_id, EchoSkillEnum.DMG)
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
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_ELEMENT.value] = element

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
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_SKILL_DMG.value] = (
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
        bonus_type = SkillBonusTypeEnum.ECHO.value
    else:
        bonus_type = resonator_skill_bonus_type
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_BONUS_TYPE.value] = (
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
            resonator_id, CalculatedResonatorColumnEnum.CALCULATED_ATK_P
        )
    )
    bonus_atk_p = get_number(row[TemplateEnum.BONUS_ATK_P])
    result_atk_p = calculated_atk_p + bonus_atk_p
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_ATK_P.value] = (
        result_atk_p
    )

    # ATK
    resonator_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorColumnEnum.ATK
        )
    )
    weapon_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorColumnEnum.WEAPON_ATK
        )
    )
    result_atk = resonator_atk + weapon_atk
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_ATK.value] = result_atk

    # Additional ATK
    echo_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorColumnEnum.ECHO_ATK
        )
    )
    template_bonus_atk = get_number(row[TemplateEnum.BONUS_ATK])
    result_atk_addition = echo_atk + template_bonus_atk
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_ATK_ADDITION.value] = (
        result_atk_addition
    )

    # CRIT Rate
    resonator_crit_rate = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorColumnEnum.CALCULATED_CRIT_RATE
        )
    )
    bonus_crit_rate = get_number(row[TemplateEnum.BONUS_CRIT_RATE])
    result_crit_rate = resonator_crit_rate + bonus_crit_rate
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_CRIT_RATE.value] = (
        result_crit_rate
    )

    # CRIT DMG
    resonator_crit_dmg = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorColumnEnum.CALCULATED_CRIT_DMG
        )
    )
    bonus_crit_dmg = get_number(row[TemplateEnum.BONUS_CRIT_DMG])
    result_crit_dmg = resonator_crit_dmg + bonus_crit_dmg
    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_CRIT_DMG.value] = (
        result_crit_dmg
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
    result_bonus = calculated_element_bonus + calculated_skill_bonus + template_bonus

    calculated_template_row_dict[CalculatedTemplateEnum.RESULT_BONUS.value] = (
        result_bonus
    )

    # Other Bonus
    bonus_magnifier = get_number(row[TemplateEnum.BONUS_MAGNIFIER])
    bonus_amplifier = get_number(row[TemplateEnum.BONUS_AMPLIFIER])
    bonus_skill_dmg_addition = get_number(row[TemplateEnum.BONUS_SKILL_DMG_ADDITION])
    bonus_ignore_def = get_number(row[TemplateEnum.BONUS_IGNORE_DEF])
    bonus_reduce_res = get_number(row[TemplateEnum.BONUS_REDUCE_RES])

    # DMG
    if resonator_skill_base_attr == ResonatorSkillBaseAttrEnum.ATK.value:
        region_base_attr = (
            result_atk * (get_number("1.0") + result_atk_p) + result_atk_addition
        )
    else:
        return

    region_skill_dmg = skill_dmg + bonus_skill_dmg_addition
    region_bonus_magnifier = get_number("1.0") + bonus_magnifier
    region_bonus_amplifier = get_number("1.0") + bonus_amplifier
    region_bonus = get_number("1.0") + result_bonus
    region_def = (get_number("800.0") + get_number("8.0") * resonator_level) / (
        get_number("800.0")
        + get_number("8.0") * resonator_level
        + monster_def * (1 - bonus_ignore_def)
    )
    region_bonus_reduce_res = get_number("1.0") + bonus_reduce_res - monster_res
    region_crit_dmg = result_crit_dmg
    region_crit = (
        result_crit_dmg * result_crit_rate + get_number("1.0") - result_crit_rate
    )

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


def get_tsv_damage(
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
        n = get_string(resonators_table.search(r_id, ResonatorColumnEnum.NAME))
        if n:
            resonators_name2id[n] = r_id

    results = []
    for _, row in template_table.df.iterrows():
        resonator_name = row[TemplateEnum.RESONATOR_NAME]
        resonator_id = resonators_name2id.get(resonator_name, None)
        if resonator_id is None:
            continue
        calculated_template_row_dict = get_tsv_row_damage(
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
