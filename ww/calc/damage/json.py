from typing import List, Optional

from ww.crud.template import get_template
from ww.model.buff import SkillBonusTypeEnum
from ww.model.echo import EchoSkillEnum
from ww.model.monsters import MonstersEnum
from ww.model.resonator_skill import ResonatorSkillBaseAttrEnum, ResonatorSkillEnum
from ww.model.resonators import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorsEnum,
    ResonatorsEnum,
)
from ww.model.template import (
    CalculatedTemplateEnum,
    CalculatedTemplateRowModel,
    TemplateRowBuffModel,
    TemplateRowBuffTypeEnum,
    TemplateRowModel,
)
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersTable
from ww.tables.resonator import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.utils.number import get_number, get_string


def get_buffs(row: TemplateRowModel) -> TemplateRowBuffModel:
    buffs = TemplateRowBuffModel()
    for buff in row.buffs:
        if buff.type == TemplateRowBuffTypeEnum.MAGNIFIER.value:
            buffs.bonus_magnifier += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.AMPLIFIER.value:
            buffs.bonus_amplifier += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.HP_P.value:
            buffs.bonus_hp_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.HP.value:
            buffs.bonus_hp += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ATK_P.value:
            buffs.bonus_atk_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ATK.value:
            buffs.bonus_atk += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.DEF_P.value:
            buffs.bonus_def_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.DEF.value:
            buffs.bonus_def += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.CRIT_RATE.value:
            buffs.bonus_crit_rate += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.CRIT_DMG.value:
            buffs.bonus_crit_dmg += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ADDITION.value:
            buffs.bonus_addition += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.SKILL_DMG_ADDITION.value:
            buffs.bonus_skill_dmg_addition += get_number(buff.value) * get_number(
                buff.stack
            )
        elif buff.type == TemplateRowBuffTypeEnum.IGNORE_DEF.value:
            buffs.bonus_ignore_def += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.REDUCE_RES.value:
            buffs.bonus_reduce_res += get_number(buff.value) * get_number(buff.stack)
    return buffs


def get_json_row_damage(
    row: TemplateRowModel,
    resonator_id,
    resonator_name,
    monster_id,
    monster_level,
    monster_def,
    resonators_table: ResonatorsTable,
    calculated_resonators_table: CalculatedResonatorsTable,
    echo_skill_table,
    monsters_table: MonstersTable,
    _,
) -> Optional[CalculatedTemplateRowModel]:
    if resonator_id is None:
        return

    calculated_row = CalculatedTemplateRowModel()

    calculated_row.resonator_name = resonator_name

    manual_bonus_type = get_string(row.skill_bonus_type)

    resonator_level = get_number(
        resonators_table.search(resonator_id, ResonatorsEnum.LEVEL)
    )

    # Buffs
    buffs = get_buffs(row)

    # Skill
    template_row_skill_id = row.skill_id

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

    calculated_row.skill_id = template_row_skill_id
    calculated_row.resonator_skill_level = resonator_skill_lv
    calculated_row.resonator_skill_element = resonator_skill_element
    calculated_row.resonator_skill_base_attr = resonator_skill_base_attr
    calculated_row.resonator_skill_type = resonator_skill_type
    calculated_row.resonator_skill_type_bonus = resonator_skill_bonus_type
    calculated_row.resonator_skill_dmg = resonator_skill_dmg

    # Echo Skill
    echo_skill_element = echo_skill_table.search(
        template_row_skill_id, EchoSkillEnum.ELEMENT
    )
    echo_skill_dmg = echo_skill_table.search(template_row_skill_id, EchoSkillEnum.DMG)
    if echo_skill_dmg is not None:
        echo_skill_dmg = get_number(echo_skill_dmg)

    calculated_row.echo_element = echo_skill_element
    calculated_row.echo_skill_dmg = echo_skill_dmg

    # Element
    if not ((resonator_skill_element is None) ^ (echo_skill_element is None)):
        # TODO: raise error
        # print("element")
        return

    if resonator_skill_element is None:
        element = echo_skill_element
    else:
        element = resonator_skill_element
    calculated_row.final_element = element

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
    calculated_row.final_skill_dmg = skill_dmg

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
    calculated_row.final_bonus_type = bonus_type

    # Monster
    monster_res = get_number(monsters_table.search(monster_id, f"{element}抗性"))
    calculated_row.monster_level = monster_level
    calculated_row.monster_def = monster_def
    calculated_row.monster_res = monster_res

    # ATK Percentage
    calculated_atk_p = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_ATK_P
        )
    )
    bonus_atk_p = buffs.bonus_atk_p
    final_atk_p = calculated_atk_p + bonus_atk_p
    calculated_row.final_atk_p = final_atk_p

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
    calculated_row.final_atk = final_atk

    # Additional ATK
    echo_atk = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.ECHO_ATK
        )
    )
    template_bonus_atk = buffs.bonus_atk
    final_atk_addition = echo_atk + template_bonus_atk
    calculated_row.final_atk_addition = final_atk_addition

    # CRIT Rate
    resonator_crit_rate = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_RATE
        )
    )
    bonus_crit_rate = buffs.bonus_crit_rate
    final_crit_rate = resonator_crit_rate + bonus_crit_rate
    calculated_row.final_crit_rate = final_crit_rate

    # CRIT DMG
    resonator_crit_dmg = get_number(
        calculated_resonators_table.search(
            resonator_id, CalculatedResonatorsEnum.CALCULATED_CRIT_DMG
        )
    )
    bonus_crit_dmg = buffs.bonus_crit_dmg
    final_crit_dmg = resonator_crit_dmg + bonus_crit_dmg
    calculated_row.final_crit_dmg = final_crit_dmg

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

    template_bonus = buffs.bonus_addition
    final_bonus = calculated_element_bonus + calculated_skill_bonus + template_bonus

    calculated_row.final_bonus = final_bonus

    # Other Bonus
    bonus_magnifier = buffs.bonus_magnifier
    bonus_amplifier = buffs.bonus_amplifier
    bonus_skill_dmg_addition = buffs.bonus_skill_dmg_addition
    bonus_ignore_def = buffs.bonus_ignore_def
    bonus_reduce_res = buffs.bonus_reduce_res

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

    calculated_row.damage = dmg_avg
    calculated_row.damage_no_crit = dmg_no_crit
    calculated_row.damage_crit = dmg_crit

    return calculated_row


def get_json_damage(
    template_id: str, monster_id: str, r_id_1: str, r_id_2: str, r_id_3: str
) -> List[CalculatedTemplateRowModel]:
    calculated_rows = []

    calculated_resonators_table = CalculatedResonatorsTable()
    resonators_table = ResonatorsTable()

    monsters_table = MonstersTable()
    monster_level = get_number(monsters_table.search(monster_id, MonstersEnum.LEVEL))
    monster_def = get_number(monsters_table.search(monster_id, MonstersEnum.DEF))

    template = get_template(template_id)
    if template is None:
        return calculated_rows

    calculated_template_columns = [e.value for e in CalculatedTemplateEnum]

    echo_skill_table = EchoSkillTable()

    resonators_name2id = {}
    r_ids = [r_id_1, r_id_2, r_id_3]
    for r_id in r_ids:
        n = get_string(resonators_table.search(r_id, ResonatorsEnum.NAME))
        if n:
            resonators_name2id[n] = r_id

    for row in template.rows:
        resonator_name = row.resonator_name
        resonator_id = resonators_name2id.get(resonator_name, None)
        if resonator_id is None:
            continue
        calculated_row = get_json_row_damage(
            row,
            resonator_id,
            resonator_name,
            monster_id,
            monster_level,
            monster_def,
            resonators_table,
            calculated_resonators_table,
            echo_skill_table,
            monsters_table,
            calculated_template_columns,
        )
        if calculated_row is not None:
            calculated_rows.append(calculated_row)
    return calculated_rows
