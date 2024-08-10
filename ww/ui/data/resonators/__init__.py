from typing import List

from PySide2.QtWidgets import QTableWidgetItem

from ww.model.echo import EchoesEnum
from ww.model.resonators import ResonatorsEnum
from ww.tables.echo import EchoesTable
from ww.tables.resonators import ResonatorsTable
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_uneditable_cell
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


def get_echoes() -> List[str]:
    echoes_table = EchoesTable()
    echoes = echoes_table.df[EchoesEnum.ID]
    return echoes.to_list()


class QResonatorsTable(QDraggableTableWidget):
    def __init__(self):
        resonators_table = ResonatorsTable()

        data = resonators_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        self._init_combobox()
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorsEnum.ID.value,
            column_names=resonators_table.df.columns,
        )

    def _init_column_width(self):
        cols = [
            self.get_column_id(ResonatorsEnum.ID.value),
            self.get_column_id(ResonatorsEnum.ECHO_1.value),
            self.get_column_id(ResonatorsEnum.ECHO_2.value),
            self.get_column_id(ResonatorsEnum.ECHO_3.value),
            self.get_column_id(ResonatorsEnum.ECHO_4.value),
            self.get_column_id(ResonatorsEnum.ECHO_5.value),
        ]
        for col in cols:
            self.setColumnWidth(col, 400)

    def _init_combobox(self):
        self._echoes = get_echoes()

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.get_column_id(ResonatorsEnum.PREFIX.value)
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _chain_i = self.get_column_id(ResonatorsEnum.RESONANCE_CHAIN.value)
        _chain = row[_chain_i]
        if _chain:
            _id.append(f"{_chain}鏈")

        _level_i = self.get_column_id(ResonatorsEnum.LEVEL.value)
        _level = row[_level_i]
        _name_i = self.get_column_id(ResonatorsEnum.NAME.value)
        _name = row[_name_i]
        if _name:
            _id.append(_level + _name)

        _weapon_rank_i = self.get_column_id(ResonatorsEnum.WEAPON_RANK.value)
        _weapon_rank = row[_weapon_rank_i]
        if _weapon_rank:
            _id.append(f"{_weapon_rank}振")

        _weapon_level_i = self.get_column_id(ResonatorsEnum.WEAPON_LEVEL.value)
        _weapon_level = row[_weapon_level_i]
        _weapon_name_i = self.get_column_id(ResonatorsEnum.WEAPON_NAME.value)
        _weapon_name = row[_weapon_name_i]
        if _weapon_name:
            _id.append(_weapon_level + _weapon_name)

        _suffix_i = self.get_column_id(ResonatorsEnum.SUFFIX.value)
        _suffix = row[_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == ResonatorsEnum.ID.value:
            set_uneditable_cell(self, value, row, col)
        elif self.column_names[col] == ResonatorsEnum.NAME.value:
            set_resonator_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.LEVEL.value:
            set_resonator_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_CHAIN.value:
            set_resonator_chain_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.NORMAL_ATTACK_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_SKILL_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_LIBERATION_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.FORTE_CIRCUIT_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.INTRO_SKILL_LV.value:
            set_resonator_skill_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.OUTRO_SKILL_LV.value:
            set_combobox(self, row, col, value, ["1"])
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_1.value:
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_2.value:
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_NAME.value:
            set_weapon_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_LEVEL.value:
            set_weapon_level_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_RANK.value:
            set_weapon_rank_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.ECHO_1.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.ECHO_2.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.ECHO_3.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.ECHO_4.value:
            set_resonator_echo_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorsEnum.ECHO_5.value:
            set_resonator_echo_combobox(self, row, col, value)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)
