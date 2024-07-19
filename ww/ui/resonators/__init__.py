from pathlib import Path
from typing import List

from PySide2.QtWidgets import QComboBox, QCompleter, QTableWidgetItem

from ww.model.resonators import ResonatorsEnum
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.resonators import ResonatorsTable
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.table import QDraggableTableWidget


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


def set_combobox(table, row: int, column: int, name: str, names: List[str]):
    combobox = QComboBox()
    # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")
    combobox.setEditable(True)
    combobox.addItems(names)
    combobox.setCurrentText(name)

    completer = QCompleter(combobox.model())
    combobox.setCompleter(completer)
    table.setCellWidget(row, column, combobox)


class QResonatorsTable(QDraggableTableWidget):
    def __init__(self):
        resonators_table = ResonatorsTable()
        data = resonators_table.df.values.tolist()

        self.column_names = resonators_table.df.columns

        rows = len(data)
        columns = len(data[0])
        super().__init__(rows, columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_combobox()

        for row in range(rows):
            for col in range(columns):
                cell = data[row][col]
                self.set_cell(cell, row, col)

    def _init_combobox(self):
        self._resonator_names = get_resonator_names()
        self._resonator_levels = get_levels()
        self._resonator_chains = get_resonator_chains()
        self._resonator_skill_levels = get_resonator_skill_levels()
        self._inherent_skills = get_inherent_skills()
        self._weapon_names = get_weapon_names()
        self._weapon_levels = get_levels()
        self._weapon_ranks = get_weapon_ranks()

    def _row_index_ctx_fill_row(self, row):
        for col in range(len(self.column_names)):
            self.set_cell("", row, col)

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == ResonatorsEnum.NAME.value:
            set_combobox(self, row, col, value, self._resonator_names)
        elif self.column_names[col] == ResonatorsEnum.LEVEL.value:
            set_combobox(self, row, col, value, self._resonator_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_CHAIN.value:
            set_combobox(self, row, col, value, self._resonator_chains)
        elif self.column_names[col] == ResonatorsEnum.NORMAL_ATTACK_LV.value:
            set_combobox(self, row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_SKILL_LV.value:
            set_combobox(self, row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.RESONANCE_LIBERATION_LV.value:
            set_combobox(self, row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.FORTE_CIRCUIT_LV.value:
            set_combobox(self, row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.INTRO_SKILL_LV.value:
            set_combobox(self, row, col, value, self._resonator_skill_levels)
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_1.value:
            set_combobox(self, row, col, value, self._inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.INHERENT_SKILL_2.value:
            set_combobox(self, row, col, value, self._inherent_skills)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_NAME.value:
            set_combobox(self, row, col, value, self._weapon_names)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_LEVEL.value:
            set_combobox(self, row, col, value, self._weapon_levels)
        elif self.column_names[col] == ResonatorsEnum.WEAPON_RANK.value:
            set_combobox(self, row, col, value, self._weapon_ranks)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)
