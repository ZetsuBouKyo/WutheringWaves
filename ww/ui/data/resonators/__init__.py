from typing import List

from PySide2.QtWidgets import QTableWidgetItem

from ww.model.resonator import ResonatorTsvColumnEnum
from ww.tables.resonator import ResonatorsTable
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_item, set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_combobox,
    set_resonator_chain_combobox,
    set_resonator_echo_combobox,
    set_resonator_inherent_skill_combobox,
    set_resonator_level_combobox,
    set_resonator_name_combobox,
    set_resonator_skill_level_combobox,
    set_weapon_level_combobox,
    set_weapon_name_combobox,
    set_weapon_rank_combobox,
)


class QResonatorsTable(QDraggableTableWidget):
    def __init__(self):
        resonators_table = ResonatorsTable()

        data = resonators_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorTsvColumnEnum.ID.value,
            column_names=resonators_table.df.columns,
        )

    def _init_column_width(self):
        cols = [
            self.get_column_id(ResonatorTsvColumnEnum.ID.value),
            self.get_column_id(ResonatorTsvColumnEnum.ECHO_1.value),
            self.get_column_id(ResonatorTsvColumnEnum.ECHO_2.value),
            self.get_column_id(ResonatorTsvColumnEnum.ECHO_3.value),
            self.get_column_id(ResonatorTsvColumnEnum.ECHO_4.value),
            self.get_column_id(ResonatorTsvColumnEnum.ECHO_5.value),
        ]
        for col in cols:
            self.setColumnWidth(col, 400)
        col_resonator_name = self.get_column_id(ResonatorTsvColumnEnum.NAME.value)
        self.setColumnWidth(col_resonator_name, 300)

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.get_column_id(ResonatorTsvColumnEnum.PREFIX.value)
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _chain_i = self.get_column_id(ResonatorTsvColumnEnum.RESONANCE_CHAIN.value)
        _chain = row[_chain_i]
        if _chain:
            _id.append(f"{_chain}鏈")

        _level_i = self.get_column_id(ResonatorTsvColumnEnum.LEVEL.value)
        _level = row[_level_i]
        _name_i = self.get_column_id(ResonatorTsvColumnEnum.NAME.value)
        _name = row[_name_i]
        if _name:
            _id.append(_level + _name)

        _weapon_rank_i = self.get_column_id(ResonatorTsvColumnEnum.WEAPON_RANK.value)
        _weapon_rank = row[_weapon_rank_i]
        if _weapon_rank:
            _id.append(f"{_weapon_rank}振")

        _weapon_level_i = self.get_column_id(ResonatorTsvColumnEnum.WEAPON_LEVEL.value)
        _weapon_level = row[_weapon_level_i]
        _weapon_name_i = self.get_column_id(ResonatorTsvColumnEnum.WEAPON_NAME.value)
        _weapon_name = row[_weapon_name_i]
        if _weapon_name:
            _id.append(_weapon_level + _weapon_name)

        _suffix_i = self.get_column_id(ResonatorTsvColumnEnum.SUFFIX.value)
        _suffix = row[_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == ResonatorTsvColumnEnum.ID.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.NAME.value:
            set_resonator_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.LEVEL.value:
            set_resonator_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.RESONANCE_CHAIN.value:
            set_resonator_chain_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.NORMAL_ATTACK_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.RESONANCE_SKILL_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == ResonatorTsvColumnEnum.RESONANCE_LIBERATION_LV.value
        ):
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.FORTE_CIRCUIT_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.INTRO_SKILL_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.OUTRO_SKILL_LV.value:
            set_combobox(self, row, col, value, ["1"])
        elif self.column_names[col] == ResonatorTsvColumnEnum.INHERENT_SKILL_1.value:
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.INHERENT_SKILL_2.value:
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.WEAPON_NAME.value:
            set_weapon_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.WEAPON_LEVEL.value:
            set_weapon_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.WEAPON_RANK.value:
            set_weapon_rank_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.ECHO_1.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.ECHO_2.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.ECHO_3.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.ECHO_4.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorTsvColumnEnum.ECHO_5.value:
            set_resonator_echo_combobox(self, row, col, value)
        else:
            set_item(self, row, col, value)
