from typing import Any, Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

UNEDITABLE_CELL_COLOR = (248, 248, 248)


def set_item(
    table: QTableWidget, row: int, col: int, value: str
) -> Optional[QTableWidgetItem]:
    if row >= table.rowCount() or col >= table.columnCount():
        return
    item = QTableWidgetItem(value)
    item.setToolTip(value)
    table.setItem(row, col, item)
    return item


def set_uneditable_cell(
    table: QTableWidget, row: int, col: int, value: Any
) -> QTableWidgetItem:
    if value is None:
        value = ""
    elif type(value) is not str:
        value = str(value)

    item_color = QColor(*UNEDITABLE_CELL_COLOR)
    item = QTableWidgetItem(value)
    item.setBackgroundColor(item_color)
    item.setFlags(~Qt.ItemIsEditable)
    item.setToolTip(value)
    table.setItem(row, col, item)
    return item
