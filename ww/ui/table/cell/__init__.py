from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

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
