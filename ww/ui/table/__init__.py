import sys
from copy import deepcopy
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
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
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

        self._history = [deepcopy(self.data)]
        self._save_event = None

        self._init_cells()
        self._init_column_width()
        self.itemChanged.connect(self._update_data)

        self.setHorizontalHeaderLabels(self.column_names)

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

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copied_cells = sorted(self.selectedIndexes())
        elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            r = self.currentRow() - self.copied_cells[0].row()
            c = self.currentColumn() - self.copied_cells[0].column()
            for cell in self.copied_cells:
                self.set_cell(
                    self.get_cell(cell.row(), cell.column()),
                    cell.row() + r,
                    cell.column() + c,
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
        selected_rows = self.get_selected_rows()
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

    def _update_data(self, item):
        print("update")

    def get_selected_rows(self) -> List[int]:
        return sorted(set(item.row() for item in self.selectedIndexes()))

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

    def _progress_init(self):
        self.progress_value = 0.0
        if self.progress is not None:
            self.progress.setValue(self.progress_value)

        self.progress_row_tick = 100.0 / (self.rowCount() + 1)

    def _progress_update_row(self):
        self.progress_value += self.progress_row_tick
        if self.progress is not None:
            self.progress.setValue(self.progress_value)

    def _progress_set_value(self, value: int):
        if self.progress is not None:
            self.progress.setValue(value)

    def save(self):
        self._progress_init()

        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.data[row][col] = self.get_cell(row, col)
            id_col = self.column_names_table[self.column_id_name]
            id = self.get_row_id(row)
            if id is not None:
                self.data[row][id_col] = id

            self._progress_update_row()

        if self.tsv_fpath is not None:
            save_tsv(self.tsv_fpath, self.data, self.column_names)

        self._progress_set_value(100)

        self._init_cells()

        if self._save_event is not None:
            self._save_event()

    def initialize(self):
        self.data = self._history[0]
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = len(self.data)
        columns = len(self.data[0])
        self.setRowCount(rows)
        self.setColumnCount(columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_cells()
        self._init_column_width()


def _table_event_show_header_context_menu(self: "QDraggableDataTableWidget", position):
    header = self._table.verticalHeader()
    row = header.logicalIndexAt(position)

    menu = QMenu()
    add_above_action = QAction("Add rows above", self)
    add_below_action = QAction("Add rows below", self)
    delete_selected_rows_action = QAction("Delete selected rows", self)
    menu.addAction(add_above_action)
    menu.addAction(add_below_action)
    menu.addAction(delete_selected_rows_action)

    add_above_action.triggered.connect(
        lambda: self._table_row_index_ctx_add_rows_above(row)
    )
    add_below_action.triggered.connect(
        lambda: self._table_row_index_ctx_add_rows_below(row)
    )
    delete_selected_rows_action.triggered.connect(
        self._table_row_index_ctx_delete_selected_rows
    )

    menu.exec_(header.viewport().mapToGlobal(position))


class QDraggableDataTableWidget(QWidget):
    def __init__(
        self,
        rows: int,
        columns: int,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
        tsv_fpath: Union[str, Path] = None,
        event_save=None,
    ):
        super().__init__()
        # Buttons
        self._layout_btns = QHBoxLayout()
        self._btn_initialize = QPushButton("初始化")
        self._btn_initialize.clicked.connect(self._table_event_initialize)
        self._btn_save = QPushButton("存檔")
        self._btn_save.clicked.connect(self._table_event_save)

        self._layout_btns.addStretch()
        self._layout_btns.addWidget(self._btn_initialize)
        self._layout_btns.addWidget(self._btn_save)

        # Progress
        self._layout_progress = QHBoxLayout()
        self._progress_bar = QProgressBar()
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(100)
        self._layout_progress.addStretch()
        self._layout_progress.addWidget(self._progress_bar)

        # Table
        self._data = data
        self._column_id_name = column_id_name
        self._column_names = column_names
        self._table_init_column_names_table()
        self._tsv_fpath = tsv_fpath

        self._table = QTableWidget(rows, columns)
        self._table.dropEvent = self._table_event_drop
        self._table.keyPressEvent = self._table_event_key_press
        self._table_init()

        # Layout
        self._layout = QVBoxLayout()
        self._layout.addLayout(self._layout_btns)
        self._layout.addWidget(self._table)
        self._layout.addLayout(self._layout_progress)
        self.setLayout(self._layout)

        self._history = [deepcopy(self._data)]
        self._event_save = event_save

        self._table_cells_init()
        self._table_columns_width()

    def _table_init(self):
        self._table.setDragEnabled(True)
        self._table.setAcceptDrops(True)
        self._table.viewport().setAcceptDrops(True)
        self._table.setDragDropOverwriteMode(False)
        self._table.setDropIndicatorShown(True)
        self._table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setDragDropMode(QAbstractItemView.InternalMove)

        # Connect context menu for vertical header
        self._table.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.verticalHeader().customContextMenuRequested.connect(
            self._table_event_show_header_context_menu
        )

        self._table.setHorizontalHeaderLabels(self._column_names)
        # self._table.itemChanged.connect(self._table_update_data)

    def _table_init_column_names_table(self):
        self._column_names_table = {
            self._column_names[i]: i for i in range(len(self._column_names))
        }

    def _table_columns_width(self): ...

    def _table_cells_init(self):
        for row in range(self._table.rowCount()):
            for col in range(self._table.columnCount()):
                cell = self._data[row][col]
                self._table_set_cell(cell, row, col)

    def _table_event_initialize(self):
        self._data = self._history[0]
        self._table_init_column_names_table()

        rows = len(self.data)
        columns = len(self.data[0])
        self._table.setRowCount(rows)
        self._table.setColumnCount(columns)

        self._table.setHorizontalHeaderLabels(self.column_names)

        self._table_cells_init()
        self._table_columns_width()

    def _table_event_save(self):
        self._progress_bar_init()

        for row in range(self._table.rowCount()):
            for col in range(self._table.columnCount()):
                self._data[row][col] = self._table_get_cell(row, col)
            id_col = self._column_names_table[self._column_id_name]
            id = self._table_get_row_id(row)
            if id is not None:
                self._data[row][id_col] = id

            self._progress_bar_update_row()

        if self.tsv_fpath is not None:
            save_tsv(self.tsv_fpath, self.data, self._column_names)

        self._progress_bar.setValue(100)

        self._table_cells_init()

        if self._event_save is not None:
            self._event_save()

    def _table_event_drop(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self._table_event_drop_on(event)

            rows = self._table_get_selected_rows()
            rows_to_move = [
                [
                    self._table_get_cell(row, col)
                    for col in range(self._table.columnCount())
                ]
                for row in rows
            ]
            for row in reversed(rows):
                self._table.removeRow(row)
                if row < drop_row:
                    drop_row -= 1

            for row, data in enumerate(rows_to_move):
                row += drop_row
                self._table.insertRow(row)
                for col, column_data in enumerate(data):
                    self._table_set_cell(column_data, row, col)

            event.accept()
            for row in range(len(rows_to_move)):
                self._table.item(drop_row + row, 0).setSelected(True)
                self._table.item(drop_row + row, 1).setSelected(True)
        super(QTableWidget, self._table).dropEvent(event)

    def _table_event_drop_on(self, event):
        index = self._table.indexAt(event.pos())
        if not index.isValid():
            return self._table.rowCount()

        return (
            index.row() + 1
            if self._table_event_drop_is_below(event.pos(), index)
            else index.row()
        )

    def _table_event_drop_is_below(self, pos, index):
        rect = self._table.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return (
            rect.contains(pos, True)
            and not (int(self._table.model().flags(index)) & Qt.ItemIsDropEnabled)
            and pos.y() >= rect.center().y()
        )

    def _table_event_key_press(self, event):
        self._table.keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self._table_copied_cells = sorted(self._table.selectedIndexes())
        elif event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            r = self._table.currentRow() - self._table_copied_cells[0].row()
            c = self._table.currentColumn() - self._table_copied_cells[0].column()
            for cell in self._table_copied_cells:
                self._table_set_cell(
                    self._table_get_cell(cell.row(), cell.column()),
                    cell.row() + r,
                    cell.column() + c,
                )

    def _table_event_show_header_context_menu(self, position):
        header = self._table.verticalHeader()
        row = header.logicalIndexAt(position)

        menu = QMenu()
        add_above_action = QAction("Add rows above", self)
        add_below_action = QAction("Add rows below", self)
        delete_selected_rows_action = QAction("Delete selected rows", self)
        menu.addAction(add_above_action)
        menu.addAction(add_below_action)
        menu.addAction(delete_selected_rows_action)

        add_above_action.triggered.connect(
            lambda: self._table_row_index_ctx_add_rows_above(row)
        )
        add_below_action.triggered.connect(
            lambda: self._table_row_index_ctx_add_rows_below(row)
        )
        delete_selected_rows_action.triggered.connect(
            self._table_row_index_ctx_delete_selected_rows
        )

        menu.exec_(header.viewport().mapToGlobal(position))

    def _table_set_id_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        item.setFlags(~Qt.ItemIsEditable)
        self._table.setItem(row, col, item)

    def _table_set_cell(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        self._table.setItem(row, col, item)

    def _table_set_combobox(
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

        self._table.setCellWidget(row, column, combobox)

    def _table_set_uneditable_cell(
        self, row: int, column: int, name: str, names: List[str]
    ):
        combobox = QCustomComboBox()
        # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")
        combobox.setEditable(True)
        combobox.addItems(names)
        combobox.setCurrentText(name)

        completer = QCompleter(combobox.model())
        combobox.setCompleter(completer)
        self._table.setCellWidget(row, column, combobox)

    def _table_row_index_ctx_fill_row(self, row):
        for col in range(len(self._column_names)):
            self._table_set_cell("", row, col)

    def _table_row_index_ctx_add_rows(self, row):
        num_rows, ok = QInputDialog.getInt(
            self, "Number of Rows", "Enter number of rows to add:", 1, 1
        )
        if ok:
            for _ in range(num_rows):
                self._table.insertRow(row)
                self._table_row_index_ctx_fill_row(row)

    def _table_row_index_ctx_add_rows_above(self, row):
        self._table_row_index_ctx_add_rows(row)

    def _table_row_index_ctx_add_rows_below(self, row):
        self._table_row_index_ctx_add_rows(row + 1)

    def _table_row_index_ctx_delete_selected_rows(self):
        selected_rows = self._table_get_selected_rows()
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
                self._table.removeRow(row)

    def _table_update_data(self, item):
        print("update")

    def _table_get_selected_rows(self) -> List[int]:
        return sorted(set(item.row() for item in self._table.selectedIndexes()))

    def _table_get_row_id(self) -> str:
        return None

    def _table_get_cell(self, row: int, col: int) -> str:
        item = self._table.item(row, col)
        cell = self._table.cellWidget(row, col)
        if item is not None:
            return item.text()
        elif cell is not None:
            return cell.currentText()
        return ""

    def _progress_bar_init(self):
        self._progress_bar_value = 0.0
        self._progress_bar.setValue(self._progress_bar_value)

        self._progress_bar_row_tick = 100.0 / (self._table.rowCount() + 1)

    def _progress_bar_update_row(self):
        self._progress_bar_value += self._progress_bar_row_tick
        self._progress_bar.setValue(self._progress_bar_value)
