from typing import Any, List, Optional

from PySide2.QtWidgets import QTableWidget

from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table.cell import set_item
from ww.ui.table.uneditable import QUneditableDataFrameTable, QUneditableTable


class QBaseTableWidget(QTableWidget):
    def __init__(self, rows: int, columns: int, parent: Any = None):
        super().__init__(rows, columns, parent=parent)

    def set_cell(self, row: int, col: int, value: str):
        set_item(self, row, col, value)

    def set_row(self, row: int, data: List[Any]):
        for col, column_data in enumerate(data):
            self.set_cell(row, col, column_data)

    def get_cell(self, row: int, col: int) -> str:
        item = self.item(row, col)
        cell = self.cellWidget(row, col)
        if item is not None:
            return item.text()
        elif type(cell) == QAutoCompleteComboBox:
            return cell.currentText()
        return ""

    def get_selected_row(self) -> Optional[int]:
        selected_rows = self.get_selected_rows()
        if len(selected_rows) != 1:
            return
        return selected_rows[0]

    def get_selected_rows(self) -> List[int]:
        return sorted(set(item.row() for item in self.selectedIndexes()))

    def get_row(self, row: int):
        return [self.get_cell(row, col) for col in range(self.columnCount())]

    def get_data(self):
        return [self.get_row(row) for row in range(self.rowCount())]

    def get_empty_data(self, row_count: int = 1) -> List[List[str]]:
        return [["" for _ in range(self.columnCount())] for _ in range(row_count)]
