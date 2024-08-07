import sys
from copy import deepcopy
from functools import partial
from pathlib import Path
from tkinter import Tk
from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd
from PySide2.QtCore import QModelIndex, Qt
from PySide2.QtGui import QColor, QDropEvent
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
from ww.utils.sorting import alphanum_sorting

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]

UNEDITABLE_CELL_COLOR = (248, 248, 248)


def set_uneditable_cell(
    table: QTableWidget, value: str, row: int, col: int
) -> QTableWidgetItem:
    item_color = QColor(*UNEDITABLE_CELL_COLOR)
    item = QTableWidgetItem(value)
    item.setBackgroundColor(item_color)
    item.setFlags(~Qt.ItemIsEditable)
    table.setItem(row, col, item)
    return item


class QUneditableDataFrameTable(QTableWidget):
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

        self._init_cells()
        self._init_column_width()

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def _init_column_width(self):
        for col_name, col_index in self.column_names_table.items():
            width = len(col_name) * 20
            self.setColumnWidth(col_index, width)

    def set_cell(self, value: str, row: int, col: int):
        set_uneditable_cell(self, value, row, col)

    def load_data(self, data: List[Dict[str, str]]):
        new_data = []
        for row in data:
            r = [row.get(column_name, "") for column_name in self.column_names]
            new_data.append(r)

        self.data = new_data

        rows = len(self.data)
        columns = len(self.data[0])
        self.setRowCount(rows)
        self.setColumnCount(columns)

        self._init_cells()

    def get_column_id(self, col_name: str) -> int:
        return self.column_names_table[col_name]


class QCustomTableWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, parent: Any = None):
        super().__init__(rows, columns, parent=parent)

    def set_cell(self, value: str, row: int, col: int):
        if row >= self.rowCount() or col >= self.columnCount():
            return
        item = QTableWidgetItem(value)
        self.setItem(row, col, item)

    def set_row(self, row: int, data: List[Any]):
        for col, column_data in enumerate(data):
            self.set_cell(column_data, row, col)

    def set_item(self, value: str, row: int, col: int):
        item = QTableWidgetItem(value)
        self.setItem(row, col, item)

    def set_combobox(
        self,
        row: int,
        column: int,
        value: str,
        options: List[str],
        currentIndexChanged=None,
        getOptions=None,
        toolTip: Optional[str] = None,
    ) -> QCustomComboBox:
        if getOptions is None:
            combobox = QCustomComboBox()
            combobox.addItems(options)
        else:
            combobox = QCustomComboBox(getOptions=getOptions)

        if toolTip is None:
            combobox.setToolTip(value)
        else:
            combobox.setToolTip(toolTip)

        combobox.setCurrentText(value)

        # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")

        if currentIndexChanged is not None:
            combobox.currentIndexChanged.connect(
                partial(currentIndexChanged, row, column, options)
            )

        self.setCellWidget(row, column, combobox)
        return combobox

    def get_cell(self, row: int, col: int) -> Optional[str]:
        item = self.item(row, col)
        cell = self.cellWidget(row, col)
        if item is not None:
            return item.text()
        elif type(cell) == QCustomComboBox:
            return cell.currentText()
        return None

    def get_selected_rows(self) -> List[int]:
        return sorted(set(item.row() for item in self.selectedIndexes()))

    def get_row(self, row: int):
        return [self.get_cell(row, col) for col in range(self.columnCount())]

    def get_data(self):
        return [self.get_row(row) for row in range(self.rowCount())]


class QDraggableTableWidget(QCustomTableWidget):
    def __init__(
        self,
        rows: int,
        columns: int,
        data: List[List[str]] = [],
        column_id_name: str = None,
        column_names: List[str] = [],
    ):
        super().__init__(rows, columns)

        self.data = data
        self.column_id_name = column_id_name
        self.column_names = column_names
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

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

        self.data_0 = [deepcopy(self.data)]

        self._init_cells()
        self._init_column_width()
        # self.itemChanged.connect(self._update_data)

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
            rows_to_move = [self.get_row(row) for row in rows]
            for row in reversed(rows):
                self.removeRow(row)
                if row < drop_row:
                    drop_row -= 1

            for row, data in enumerate(rows_to_move):
                row += drop_row
                self.insertRow(row)
                self.set_row(row, data)

            event.accept()
            for row in range(len(rows_to_move)):
                item_1 = self.item(drop_row + row, 0)
                if item_1 is not None:
                    item_1.setSelected(True)
                item_2 = self.item(drop_row + row, 1)
                if item_2 is not None:
                    item_2.setSelected(True)
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

    def _to_clipboard(self):
        if not hasattr(self, "copied_cells"):
            return

        line = []
        lines = []
        row = self.copied_cells[0].row()
        for cell in self.copied_cells:
            r = cell.row()
            c = cell.column()
            if row != r:
                lines.append("\t".join(line))
                line = []
                row = r

            line.append(self.get_cell(r, c))

        lines.append("\t".join(line))

        text = "\n".join(lines)
        tk = Tk()
        tk.clipboard_clear()
        tk.clipboard_append(text)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copied_cells = sorted(self.selectedIndexes())
            self._to_clipboard()
            return
        if event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier):
            if hasattr(self, "copied_cells"):
                r = self.currentRow() - self.copied_cells[0].row()
                c = self.currentColumn() - self.copied_cells[0].column()
                for cell in self.copied_cells:
                    new_row = cell.row() + r
                    new_col = cell.column() + c

                    if new_row >= self.rowCount() or new_col >= self.columnCount():
                        continue

                    self.set_cell(
                        self.get_cell(cell.row(), cell.column()), new_row, new_col
                    )
            else:
                text = Tk().clipboard_get()
                lines = text.split("\n")
                for i in range(len(lines)):
                    line = lines[i].split("\t")
                    lines[i] = line
                # print(lines)
                current_row = self.currentRow()
                current_col = self.currentColumn()
                for row in range(len(lines)):
                    for col in range(len(lines[row])):
                        self.set_cell(
                            lines[row][col], row + current_row, col + current_col
                        )

    def show_header_context_menu(self, position):
        header = self.verticalHeader()
        row = header.logicalIndexAt(position)

        menu = QMenu()
        add_above_action = QAction("向上插入列", self)
        add_below_action = QAction("向下插入列", self)

        menu.addAction(add_above_action)
        menu.addAction(add_below_action)

        if len(self.get_selected_rows()) > 0:
            delete_selected_rows_action = QAction("刪除所選擇的列", self)
            menu.addAction(delete_selected_rows_action)
            delete_selected_rows_action.triggered.connect(
                self._row_index_ctx_delete_selected_rows
            )

        add_above_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_above(row)
        )
        add_below_action.triggered.connect(
            lambda: self._row_index_ctx_add_rows_below(row)
        )

        menu.exec_(header.viewport().mapToGlobal(position))

    def set_id_cell(self, value: str, row: int, col: int) -> QTableWidgetItem:
        return set_uneditable_cell(self, value, row, col)

    def set_uneditable_cell(self, value: str, row: int, col: int) -> QTableWidgetItem:
        return set_uneditable_cell(self, value, row, col)

    def _row_index_ctx_fill_row(self, row):
        for col in range(len(self.column_names)):
            self.set_cell("", row, col)

    def _row_index_ctx_add_rows(self, row):
        dialog = QInputDialog()
        num_rows, ok = dialog.getInt(self, "插入列", "插入多少列:", 1, 1)
        if ok:
            for n in range(num_rows):
                new_row = row + n
                self.insertRow(new_row)
                self._row_index_ctx_fill_row(new_row)

    def _row_index_ctx_add_rows_above(self, row):
        self._row_index_ctx_add_rows(row)

    def _row_index_ctx_add_rows_below(self, row):
        self._row_index_ctx_add_rows(row + 1)

    def _row_index_ctx_delete_selected_rows(self):
        selected_rows = self.get_selected_rows()
        selected_rows_str = ", ".join([str(i + 1) for i in selected_rows])

        if not selected_rows:
            QMessageBox.warning(self, "警告", "沒有可刪除的列。")
            return

        confirmation = QMessageBox.question(
            self,
            "刪除列",
            f"你確定要刪除第 {selected_rows_str} 列？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            for row in reversed(selected_rows):
                self.removeRow(row)

    # def _update_data(self, item):
    #     print("update")

    def get_row_id(self, row) -> str:
        return None

    def get_current_data(self) -> List[List[str]]:
        data = []
        for row in range(self.rowCount()):
            r = [self.get_cell(row, col) for col in range(self.columnCount())]
            data.append(r)
        return data

    def get_column_id(self, col_name: str) -> int:
        return self.column_names_table[col_name]


class QDraggableDataTableWidget(QWidget):

    def __init__(
        self,
        table: QDraggableTableWidget,
        tsv_fpath: Union[str, Path] = None,
        event_save_after: Callable[[], None] = None,
        event_save_row_before: Callable[[int], None] = None,
    ):
        super().__init__()
        # Buttons
        self._layout_btns = QHBoxLayout()
        self._btn_initialize = QPushButton("初始化")
        self._btn_initialize.clicked.connect(self.initialize)
        self._btn_save = QPushButton("存檔")
        self._btn_save.clicked.connect(self.save)

        self._layout_btns.addStretch()
        self._layout_btns.addWidget(self._btn_initialize)
        self._layout_btns.addWidget(self._btn_save)

        # Progress
        self._layout_progress = QHBoxLayout()
        self._progress_label = QLabel("")
        self._progress_label.setFixedWidth(150)
        self._progress_bar = QProgressBar()
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(100)
        self._layout_progress.addStretch()
        self._layout_progress.addWidget(self._progress_label)
        self._layout_progress.addWidget(self._progress_bar)

        # Table
        self._table = table

        # Layout
        self._layout = QVBoxLayout()
        self._layout.addLayout(self._layout_btns)
        self._layout.addWidget(self._table)
        self._layout.addLayout(self._layout_progress)
        self.setLayout(self._layout)

        self._lock = False
        self._tsv_fpath = tsv_fpath
        self._event_save_after = event_save_after
        self._event_save_row_before = event_save_row_before

    def _progress_bar_init(self):
        self._progress_bar_value = 0.0
        self._progress_bar.setValue(self._progress_bar_value)

        self._progress_bar_row_tick = 100.0 / (self._table.rowCount() + 1)

    def _progress_bar_update_row(self):
        self._progress_bar_value += self._progress_bar_row_tick
        self._progress_bar.setValue(self._progress_bar_value)

    def save(self):
        if self._lock:
            return
        self._lock = True
        self._progress_label.setText("存檔中...")

        self._progress_bar_init()
        _ids = {}
        _dup_ids = set()
        _new_data = []
        for row in range(self._table.rowCount()):
            if self._event_save_row_before is not None:
                self._event_save_row_before(row)

            _new_data_row = ["" for _ in range(self._table.columnCount())]
            for col in range(self._table.columnCount()):
                _new_data_row[col] = self._table.get_cell(row, col)

            id_col = self._table.get_column_id(self._table.column_id_name)
            id = self._table.get_row_id(_new_data_row)
            if id in _ids:
                _dup_ids.add(str(_ids[id] + 1))
                _dup_ids.add(str(row + 1))
            if id != "":
                _ids[id] = row

            if id is not None:
                _new_data_row[id_col] = id

            _new_data.append(_new_data_row)

            self._progress_bar_update_row()
        if len(_dup_ids) > 0:
            _dup_ids = list(_dup_ids)
            _dup_ids = alphanum_sorting(_dup_ids)
            ids_str = ", ".join(_dup_ids)

            QMessageBox.question(
                self,
                "警告",
                f"'{self._table.column_id_name}'中，第{ids_str}列字串重複，請加入字首或字尾，使'{self._table.column_id_name}'中的字串不重複。",
                QMessageBox.Yes,
            )
            self._progress_label.setText("")
            self._progress_bar.setValue(0.0)
            self._lock = False
            return

        self._table.data = _new_data
        if self._tsv_fpath is not None:
            save_tsv(self._tsv_fpath, self._table.data, self._table.column_names)

        self._progress_bar_update_row()

        self._table._init_cells()

        if self._event_save_after is not None:
            self._event_save_after()

        self._lock = False
        self._progress_bar.setValue(100)
        self._progress_label.setText("存檔完成。")

    def initialize(self):
        if self._lock:
            return
        self._lock = True
        self._progress_label.setText("初始化...")

        self._progress_bar_init()

        self._table.data = self._table.data_0[0]
        self._table.column_names_table = {
            self._table.column_names[i]: i for i in range(len(self._table.column_names))
        }

        rows = len(self._table.data)
        columns = len(self._table.data[0])
        self._table.setRowCount(rows)
        self._table.setColumnCount(columns)

        self._table.setHorizontalHeaderLabels(self._table.column_names)
        self._progress_bar.setValue(10)

        self._table._init_cells()
        self._table._init_column_width()

        self._progress_bar.setValue(100)
        self._lock = False
        self._progress_label.setText("初始化完成。")
