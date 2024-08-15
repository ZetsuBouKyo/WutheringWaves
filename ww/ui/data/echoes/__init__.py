from typing import List

from PySide2.QtWidgets import QTableWidgetItem

from ww.model.echo import EchoTsvColumnEnum, ResonatorEchoTsvColumnEnum
from ww.tables.echo import EchoesTable, EchoListTable
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_item, set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_echo_name_combobox,
    set_echo_sonata_combobox,
    set_element_combobox,
)


class QEchoesTable(QDraggableTableWidget):
    def __init__(self):
        self.echoes_table = EchoesTable()
        self.echo_list_table = EchoListTable()

        data = self.echoes_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorEchoTsvColumnEnum.ID.value,
            column_names=self.echoes_table.df.columns,
        )

    def _init_column_width(self):
        col = self.get_column_id(ResonatorEchoTsvColumnEnum.ID.value)
        self.setColumnWidth(col, 400)

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.get_column_id(ResonatorEchoTsvColumnEnum.PREFIX.value)
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _element_i = self.get_column_id(ResonatorEchoTsvColumnEnum.ELEMENT.value)
        _element = row[_element_i]
        if _element:
            _id.append(_element)

        _name_i = self.get_column_id(ResonatorEchoTsvColumnEnum.NAME.value)
        _name = row[_name_i]
        if _name:
            _id.append(_name)

        _suffix_i = self.get_column_id(ResonatorEchoTsvColumnEnum.SUFFIX.value)
        _suffix = row[_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def set_row_cost(self, row: int):
        col_name = self.get_column_id(ResonatorEchoTsvColumnEnum.NAME.value)
        echo_name = self.get_cell(row, col_name)
        if not echo_name:
            return
        echo_cost = self.echo_list_table.search(echo_name, EchoTsvColumnEnum.COST)
        if not echo_cost:
            return

        col_cost = self.get_column_id(ResonatorEchoTsvColumnEnum.COST.value)
        set_uneditable_cell(self, row, col_cost, echo_cost)

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == ResonatorEchoTsvColumnEnum.ID.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == ResonatorEchoTsvColumnEnum.COST.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == ResonatorEchoTsvColumnEnum.NAME.value:
            set_echo_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorEchoTsvColumnEnum.ELEMENT.value:
            set_element_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorEchoTsvColumnEnum.ECHO_SONATA.value:
            set_echo_sonata_combobox(self, row, col, value)
        else:
            set_item(self, row, col, value)
