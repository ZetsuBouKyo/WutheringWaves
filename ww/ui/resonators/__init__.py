from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QCompleter, QTableWidgetItem

from ww.model.resonators import ResonatorsEnum
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.resonators import RESONATORS_PATH, ResonatorsTable
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget
from ww.utils.pd import save_tsv


def get_resonator_names() -> List[str]:
    home_path = Path(RESONATOR_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_resonator_chains() -> List[str]:
    return [str(i) for i in range(1, 7)]


def get_resonator_skill_levels() -> List[str]:
    return [str(i) for i in range(1, 11)]


def get_inherent_skills() -> List[str]:
    return ["0", "1"]


def get_levels() -> List[str]:
    levels = [str(i) for i in range(10, 100, 10)] + [
        "1",
        "20+",
        "40+",
        "60+",
        "70+",
        "80+",
    ]
    levels.sort()
    return levels


def get_weapon_names() -> List[str]:
    home_path = Path(WEAPON_HOME_PATH)
    names = [p.name for p in home_path.glob("*")]
    return names


def get_weapon_ranks() -> List[str]:
    ranks = [str(i) for i in range(1, 6)]
    return ranks


class QResonatorsTable(QDraggableTableWidget):
    def __init__(self):
        resonators_table = ResonatorsTable()
        self.data = resonators_table.df.values.tolist()

        self.column_names = resonators_table.df.columns
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        self._rows: int = len(self.data)
        self._columns: int = len(self.data[0])
        super().__init__(self._rows, self._columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_combobox()
        self._init_cells()

    def _init_combobox(self):
        self._resonator_names = get_resonator_names()
        self._resonator_levels = get_levels()
        self._resonator_chains = get_resonator_chains()
        self._resonator_skill_levels = get_resonator_skill_levels()
        self._inherent_skills = get_inherent_skills()
        self._weapon_names = get_weapon_names()
        self._weapon_levels = get_levels()
        self._weapon_ranks = get_weapon_ranks()

    def _init_cells(self):
        for row in range(self._rows):
            for col in range(self._columns):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def _row_index_ctx_fill_row(self, row):
        for col in range(len(self.column_names)):
            self.set_cell("", row, col)

    def get_row_id(self, row: int) -> str:
        _id = []

        _prefix_i = self.column_names_table[ResonatorsEnum.PREFIX.value]
        _prefix = self.data[row][_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _chain_i = self.column_names_table[ResonatorsEnum.RESONANCE_CHAIN.value]
        _chain = self.data[row][_chain_i]
        if _chain:
            _id.append(f"{_chain}鏈")

        _level_i = self.column_names_table[ResonatorsEnum.LEVEL.value]
        _level = self.data[row][_level_i]
        _name_i = self.column_names_table[ResonatorsEnum.NAME.value]
        _name = self.data[row][_name_i]
        if _name:
            _id.append(_level + _name)

        _weapon_rank_i = self.column_names_table[ResonatorsEnum.WEAPON_RANK.value]
        _weapon_rank = self.data[row][_weapon_rank_i]
        if _weapon_rank:
            _id.append(f"{_weapon_rank}振")

        _weapon_level_i = self.column_names_table[ResonatorsEnum.WEAPON_LEVEL.value]
        _weapon_level = self.data[row][_weapon_level_i]
        _weapon_name_i = self.column_names_table[ResonatorsEnum.WEAPON_NAME.value]
        _weapon_name = self.data[row][_weapon_name_i]
        if _weapon_name:
            _id.append(_weapon_level + _weapon_name)

        _suffix_i = self.column_names_table[ResonatorsEnum.SUFFIX.value]
        _suffix = self.data[row][_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def update_row_id(self, row: int, col: int, value: str):
        prefix_col = self.column_names_table[ResonatorsEnum.PREFIX.value]
        suffix_col = self.column_names_table[ResonatorsEnum.SUFFIX.value]
        if prefix_col == col or suffix_col == col:
            return
        id_col = self.column_names_table[ResonatorsEnum.ID.value]
        self.data[row][col] = value
        id = self.get_row_id(row)
        self.set_id_cell(id, row, id_col)

    def update_row_id_by_combobox(self, row: int, col: int, values: List[str], i: int):
        self.update_row_id(row, col, values[i])

    def update_row_id_by_item(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        self.update_row_id(row, col, value)

    def set_id_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        item.setFlags(~Qt.ItemIsEditable)
        self.setItem(row, col, item)

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == ResonatorsEnum.ID.value:
            self.set_id_cell(value, row, col)

        elif self.column_names[col] == ResonatorsEnum.NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_names,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.LEVEL.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_levels,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_CHAIN.value:
            self.set_combobox(
                row,
                col,
                value,
                self._resonator_chains,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.NORMAL_ATTACK_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_SKILL_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_LIBERATION_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.FORTE_CIRCUIT_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.INTRO_SKILL_LV.value:
            self.set_combobox(row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.OUTRO_SKILL_LV.value:
            self.set_combobox(row, col, value, ["1"])
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_1.value:
            self.set_combobox(row, col, value, self._inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_2.value:
            self.set_combobox(row, col, value, self._inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_names,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.WEAPON_LEVEL.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_levels,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        elif self.column_names[col] == ResonatorsEnum.WEAPON_RANK.value:
            self.set_combobox(
                row,
                col,
                value,
                self._weapon_ranks,
                currentIndexChanged=self.update_row_id_by_combobox,
            )
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)

    def save(self):
        for row in range(self._rows):
            for col in range(self._columns):
                item = self.item(row, col)
                cell = self.cellWidget(row, col)
                if item is not None:
                    self.data[row][col] = item.text()
                elif cell is not None:
                    self.data[row][col] = cell.currentText()
            id_col = self.column_names_table[ResonatorsEnum.ID.value]
            id = self.get_row_id(row)
            self.data[row][id_col] = id

        save_tsv(RESONATORS_PATH, self.data, self.column_names)
        self._init_cells()