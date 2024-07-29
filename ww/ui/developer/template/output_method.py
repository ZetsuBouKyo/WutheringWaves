from typing import Dict, List

from PySide2.QtWidgets import QTableWidgetItem, QVBoxLayout, QWidget

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
        if self.column_names[col] == TemplateRowModelEnum.BONUS_MAGNIFIER.value:
            combo = QMultipleCheckableComboBox()
            combo.setToolTip("你好\n阿")
            combo.addItems(
                [
                    "11111111111111111111111111111111",
                    "2222222222222222 2222222222222222",
                ]
            )
            self.setCellWidget(row, col, combo)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)


class QTemplateOutputMethodTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_output_method_table = QTemplateTabOutputMethodTable()

        self.layout.addWidget(self.q_output_method_table)

        self.setLayout(self.layout)
