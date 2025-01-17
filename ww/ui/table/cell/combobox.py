from typing import List, Optional

from PySide2.QtWidgets import QTableWidget

from ww.crud import get_actions, get_buff_types, get_elements, get_skill_base_attributes
from ww.crud.buff import get_buff_sources, get_buff_targets, get_skill_bonus_types
from ww.crud.echo import (
    get_echo_affixes,
    get_echo_costs,
    get_echo_names,
    get_echo_sonatas,
    get_echoes,
)
from ww.crud.monster import get_monster_ids
from ww.crud.resonator import (
    get_resonator_base_attrs,
    get_resonator_chains,
    get_resonator_ids,
    get_resonator_inherent_skills,
    get_resonator_levels,
    get_resonator_names,
    get_resonator_skill_bonus,
    get_resonator_skill_levels,
)
from ww.crud.template import get_template_ids
from ww.crud.weapon import get_weapon_levels, get_weapon_names, get_weapon_ranks
from ww.ui.combobox.autocomplete import QAutoCompleteComboBox


def set_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    options: List[str],
    getOptions=None,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    if getOptions is None:
        combobox = QAutoCompleteComboBox()
        combobox.addItems(options)
    else:
        combobox = QAutoCompleteComboBox(getOptions=getOptions)

    if toolTip is None:
        combobox.setToolTip(value)
    else:
        combobox.setToolTip(toolTip)

    combobox.setCurrentText(value)

    # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")

    table.setCellWidget(row, column, combobox)
    return combobox


def set_resonator_primary_key_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_resonator_ids, toolTip=toolTip
    )


def set_resonator_name_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_resonator_names, toolTip=toolTip
    )


def set_resonator_level_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_resonator_levels, toolTip=toolTip
    )


def set_resonator_chain_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_resonator_chains, toolTip=toolTip
    )


def set_resonator_skill_level_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_resonator_skill_levels,
        toolTip=toolTip,
    )


def set_resonator_inherent_skill_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_resonator_inherent_skills,
        toolTip=toolTip,
    )


def set_resonator_base_attr_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_resonator_base_attrs,
        toolTip=toolTip,
    )


def set_resonator_skill_bonus_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_resonator_skill_bonus,
        toolTip=toolTip,
    )


def set_resonator_echo_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_echoes,
        toolTip=toolTip,
    )


def set_weapon_name_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_weapon_names, toolTip=toolTip
    )


def set_weapon_rank_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_weapon_ranks, toolTip=toolTip
    )


def set_weapon_level_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_weapon_levels, toolTip=toolTip
    )


def set_echo_name_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_echo_names, toolTip=toolTip
    )


def set_echo_cost_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_echo_costs, toolTip=toolTip
    )


def set_echo_affix_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_echo_affixes, toolTip=toolTip
    )


def set_echo_sonata_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_echo_sonatas, toolTip=toolTip
    )


def set_monster_primary_key_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_monster_ids, toolTip=toolTip
    )


def set_template_primary_key_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_template_ids, toolTip=toolTip
    )


def set_element_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_elements, toolTip=toolTip
    )


def set_buff_type_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_buff_types, toolTip=toolTip
    )


def set_buff_source_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_buff_sources, toolTip=toolTip
    )


def set_buff_target_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_buff_targets, toolTip=toolTip
    )


def set_action_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table, row, column, value, [], getOptions=get_actions, toolTip=toolTip
    )


def set_skill_base_attribute_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_skill_base_attributes,
        toolTip=toolTip,
    )


def set_skill_bonus_type_combobox(
    table: QTableWidget,
    row: int,
    column: int,
    value: str,
    toolTip: Optional[str] = None,
) -> QAutoCompleteComboBox:
    return set_combobox(
        table,
        row,
        column,
        value,
        [],
        getOptions=get_skill_bonus_types,
        toolTip=toolTip,
    )
