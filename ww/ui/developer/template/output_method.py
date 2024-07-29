from typing import Dict, List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ww.crud.resonator import get_resonator_names
from ww.model.template import TemplateRowModel, TemplateRowModelEnum
from ww.ui.combobox import QMultipleCheckableComboBox
from ww.ui.table import QDraggableTableWidget


class QTemplateTabOutputMethodTable(QDraggableTableWidget):
    def __init__(self, ouput_methods: List[TemplateRowModel] = []):
        column_names = [e.value for e in TemplateRowModelEnum]

        self.ouput_methods = ouput_methods
        if len(self.ouput_methods) == 0:
            data = [["" for _ in range(len(column_names))]]

        rows = len(data)
        columns = len(column_names)

        super().__init__(rows, columns, data, column_names=column_names)
        self.setHorizontalHeaderLabels(self.column_names)

    def _init_column_width(self):
        for e in TemplateRowModelEnum:
            width = len(e.value) * 20 + 50
            col = self.column_names_table[e.value]
            self.setColumnWidth(col, width)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == TemplateRowModelEnum.RESONATOR_NAME.value:
            self.set_combobox(row, col, value, [], getOptions=get_resonator_names)
        elif self.column_names[col] == TemplateRowModelEnum.BONUS_BUFF.value:
            btn = QPushButton("+")
            btn.clicked.connect(self.add_buff)
            self.setCellWidget(row, col, btn)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)

    def add_buff(self):
        width = 800
        height = 600

        center = QDesktopWidget().availableGeometry().center()

        x0 = center.x() - width // 2
        y0 = center.y() - height // 2

        dialog = QDialog(self)
        dialog.setWindowTitle("Wuthering Waves Template Buff")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(x0, y0, width, height)
        dialog.exec_()


class QTemplateOutputMethodTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_output_method_table = QTemplateTabOutputMethodTable()

        self.layout.addWidget(self.q_output_method_table)

        self.setLayout(self.layout)
