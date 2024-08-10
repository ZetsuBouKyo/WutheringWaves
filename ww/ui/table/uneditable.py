from copy import deepcopy
from pathlib import Path
from tkinter import Tk
from typing import Any, Callable, Dict, List, Optional, Set, Union

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtGui import QDropEvent
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QHBoxLayout,
    QInputDialog,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from ww.locale import ZhTwEnum, _
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.progress_bar import QHProgressBar
from ww.ui.table.cell import set_item, set_uneditable_cell
from ww.utils.pd import safe_get_df, save_tsv
from ww.utils.sorting import alphanum_sorting


class QUneditableTable(QTableWidget):
    def __init__(self, data: List[List[str]], column_names: List[str]):
        self.data = data
        self.column_names = column_names
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = len(self.data)
        columns = len(self.data[0])
        super().__init__(rows, columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_cells()
        self._init_column_width()

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(row, col, cell)

    def _init_column_width(self):
        for col_name, col_index in self.column_names_table.items():
            width = len(col_name) * 20 + 50
            self.setColumnWidth(col_index, width)

    def set_cell(self, row: int, col: int, value: str):
        set_uneditable_cell(self, row, col, value)

    def load_list(self, data: List[List[str]]):
        self.data = data

        rows = len(self.data)
        columns = len(self.data[0])
        self.setRowCount(rows)
        self.setColumnCount(columns)

        self._init_cells()

    def load_dict(self, data: List[Dict[str, str]]):
        new_data = []
        for row in data:
            r = [row.get(column_name, "") for column_name in self.column_names]
            new_data.append(r)

        self.load_list(new_data)

    def get_column_id(self, col_name: str) -> int:
        return self.column_names_table[col_name]


class QUneditableDataFrameTable(QUneditableTable):
    def __init__(self, df: pd.DataFrame):
        data = df.values.tolist()
        column_names = df.columns

        super().__init__(data, column_names)
