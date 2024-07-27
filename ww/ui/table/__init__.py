import sys
from functools import partial
from pathlib import Path
from typing import List, Union

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtGui import QDropEvent
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCompleter,
    QHBoxLayout,
    QInputDialog,
    QMenu,
    QMessageBox,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from ww.model.echoes import EchoListEnum
from ww.tables.echoes import EchoListTable
from ww.ui.combobox import QCustomComboBox
from ww.utils.pd import save_tsv

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


class QUneditableTable(QTableWidget):
    def __init__(self, df: pd.DataFrame):
        self.data = df.values.tolist()
        self.column_names = df.columns
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

    def _init_column_width(self): ...

    def set_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        item.setFlags(~Qt.ItemIsEditable)
        self.setItem(row, col, item)


class QDraggableTableWidget(QTableWidget):

    def __init__(
        self,
        rows: int,
        columns: int,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
        tsv_fpath: Union[str, Path] = None,
        progress: QProgressBar = None,
    ):
        super().__init__(rows, columns)

        self.data = data
        self.column_id_name = column_id_name
        self.column_names = column_names
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }
        self.tsv_fpath = tsv_fpath
        self.progress = progress

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        # Connect context menu for vertical header
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(
            self.show_header_context_menu
        )

        self._init()
        self._init_column_width()
        # self.itemChanged.connect(self._update_data)

        self.setHorizontalHeaderLabels(self.column_names)

    def _init(self):
        self._save_event = None

        self._init_cells()

    def _init_column_width(self): ...

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = self.get_selected_rows()
            rows_to_move = [
                [self.get_cell(row, col) for col in range(self.columnCount())]
                for row in rows
            ]
            for row in reversed(rows):
                self.removeRow(row)
                if row < drop_row:
                    drop_row -= 1

            for row, data in enumerate(rows_to_move):
                row += drop_row
                self.insertRow(row)
                for col, column_data in enumerate(data):
                    self.set_cell(column_data, row, col)

            event.accept()
            for row in range(len(rows_to_move)):
                self.item(drop_row + row, 0).setSelected(True)
                self.item(drop_row + row, 1).setSelected(True)
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return (
            rect.contains(pos, True)
            and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled)
            and pos.y() >= rect.center().y()
        )

    def show_header_context_menu(self, position):
        header = self.verticalHeader()
        row = header.logicalIndexAt(position)

        menu = QMenu()
        add_above_action = QAction("Add rows above", self)
        add_below_action = QAction("Add rows below", self)
        delete_selected_rows_action = QAction("Delete selected rows", self)
        menu.addAction(add_above_action)
        menu.addAction(add_below_action)
        menu.addAction(delete_selected_rows_action)

        add_above_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_above(row)
        )
        add_below_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_below(row)
        )
        delete_selected_rows_action.triggered.connect(
            self._row_index_ctx_delete_selected_rows
        )

        menu.exec_(header.viewport().mapToGlobal(position))

    def set_id_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        item.setFlags(~Qt.ItemIsEditable)
        self.setItem(row, col, item)

    def set_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        self.setItem(row, col, item)

    def set_combobox(
        self,
        row: int,
        column: int,
        name: str,
        names: List[str],
        currentIndexChanged=None,
        getOptions=None,
    ):

        if getOptions is None:
            combobox = QCustomComboBox()
            combobox.addItems(names)
            combobox.setCurrentText(name)
            completer = QCompleter(combobox.model())
            combobox.setCompleter(completer)
        else:
            combobox = QCustomComboBox(getOptions=getOptions)
            combobox.setCurrentText(name)

        # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")

        if currentIndexChanged is not None:
            combobox.currentIndexChanged.connect(
                partial(currentIndexChanged, row, column, names)
            )

        self.setCellWidget(row, column, combobox)

    def set_uneditable_cell(self, row: int, column: int, name: str, names: List[str]):
        combobox = QCustomComboBox()
        # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")
        combobox.setEditable(True)
        combobox.addItems(names)
        combobox.setCurrentText(name)

        completer = QCompleter(combobox.model())
        combobox.setCompleter(completer)
        self.setCellWidget(row, column, combobox)

    def set_save_event(self, event):
        self._save_event = event

    def _row_index_ctx_fill_row(self, row):
        for col in range(len(self.column_names)):
            self.set_cell("", row, col)

    def _row_index_ctx_add_rows(self, row):
        num_rows, ok = QInputDialog.getInt(
            self, "Number of Rows", "Enter number of rows to add:", 1, 1
        )
        if ok:
            for _ in range(num_rows):
                self.insertRow(row)
                self._row_index_ctx_fill_row(row)

    def _row_index_ctx_add_rows_above(self, row):
        self._row_index_ctx_add_rows(row)

    def _row_index_ctx_add_rows_below(self, row):
        self._row_index_ctx_add_rows(row + 1)

    def _row_index_ctx_delete_selected_rows(self):
        selected_rows = sorted(set(index.row() for index in self.selectedIndexes()))
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "No rows selected to remove.")
            return

        confirmation = QMessageBox.question(
            self,
            "Remove Rows",
            f"Are you sure you want to remove {len(selected_rows)} row(s)?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            for row in reversed(selected_rows):
                self.removeRow(row)

    # def _update_data(self, item):
    #     row = item.row()
    #     col = item.column()
    #     value = item.text()
    #     self.data[row][col] = value

    def get_selected_rows(self) -> List[int]:
        return sorted(set(item.row() for item in self.selectedItems()))

    def get_row_id(self) -> str:
        return None

    def get_cell(self, row: int, col: int) -> str:
        item = self.item(row, col)
        cell = self.cellWidget(row, col)
        if item is not None:
            return item.text()
        elif cell is not None:
            return cell.currentText()
        return ""

    def save(self):
        progress_value = 0.0
        if self.progress is not None:
            self.progress.setValue(progress_value)

        progress_tick = 100.0 / (self.rowCount() + 1)

        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.data[row][col] = self.get_cell(row, col)
            id_col = self.column_names_table[self.column_id_name]
            id = self.get_row_id(row)
            if id is not None:
                self.data[row][id_col] = id

            progress_value += progress_tick
            if self.progress is not None:
                self.progress.setValue(progress_value)

        if self.tsv_fpath is not None:
            save_tsv(self.tsv_fpath, self.data, self.column_names)
        self._init()

        if self._save_event is not None:
            self._save_event()

        if self.progress is not None:
            self.progress.setValue(100)
