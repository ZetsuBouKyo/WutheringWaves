from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QCompleter,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
)

from ww.model.echoes import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.model.resonators import CalculatedResonatorsEnum
from ww.tables.echoes import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.resonators import CalculatedResonatorsTable
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


class QCalculatedResonatorsTable(QTableWidget):
    def __init__(self):
        calculated_resonators_table = CalculatedResonatorsTable()

        self.data = calculated_resonators_table.df.values.tolist()
        self.column_names = calculated_resonators_table.df.columns
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = len(self.data)
        columns = len(self.data[0])
        super().__init__(rows, columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init()
        self._init_column_width()

    def _init(self):
        self._init_cells()

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def _init_column_width(self):
        for e in CalculatedResonatorsEnum:
            if e.value == CalculatedResonatorsEnum.ID.value:
                col = self.column_names_table[e.value]
                self.setColumnWidth(col, 500)
            else:
                width = len(e.value) * 20 + 50
                col = self.column_names_table[e.value]
                self.setColumnWidth(col, width)

    def set_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        item.setFlags(~Qt.ItemIsEditable)
        self.setItem(row, col, item)
