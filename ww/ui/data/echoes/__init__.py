from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QCompleter, QProgressBar, QTableWidgetItem

from ww.crud.echo import get_echo_names, get_echo_sonatas
from ww.model.echo import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.model.element import ElementEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echo import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table import QDraggableTableWidget


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


class QEchoesTable(QDraggableTableWidget):
    def __init__(self):
        self.echoes_table = EchoesTable()
        self.echo_list_table = EchoListTable()

        data = self.echoes_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        self._init_combobox()
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoesEnum.ID.value,
            column_names=self.echoes_table.df.columns,
        )

    def _init_column_width(self):
        col = self.get_column_id(EchoesEnum.ID.value)
        self.setColumnWidth(col, 400)

    def _init_combobox(self):
        self._echo_names = get_echo_names()
        self._elements = get_elements()
        self._echo_sonatas = get_echo_sonatas()

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.get_column_id(EchoesEnum.PREFIX.value)
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _element_i = self.get_column_id(EchoesEnum.ELEMENT.value)
        _element = row[_element_i]
        if _element:
            _id.append(_element)

        _name_i = self.get_column_id(EchoesEnum.NAME.value)
        _name = row[_name_i]
        if _name:
            _id.append(_name)

        _suffix_i = self.get_column_id(EchoesEnum.SUFFIX.value)
        _suffix = row[_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def set_row_cost(self, row: int):
        col_name = self.get_column_id(EchoesEnum.NAME.value)
        echo_name = self.get_cell(row, col_name)
        if not echo_name:
            return
        echo_cost = self.echo_list_table.search(echo_name, EchoListEnum.COST)
        if not echo_cost:
            return

        col_cost = self.get_column_id(EchoesEnum.COST.value)
        self.set_uneditable_cell(echo_cost, row, col_cost)

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == EchoesEnum.ID.value:
            self.set_id_cell(value, row, col)
        elif self.column_names[col] == EchoesEnum.COST.value:
            self.set_uneditable_cell(value, row, col)
        elif self.column_names[col] == EchoesEnum.NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._echo_names,
            )
        elif self.column_names[col] == EchoesEnum.ELEMENT.value:
            self.set_combobox(
                row,
                col,
                value,
                self._elements,
            )
        elif self.column_names[col] == EchoesEnum.ECHO_SONATA.value:
            self.set_combobox(
                row,
                col,
                value,
                self._echo_sonatas,
            )
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)
