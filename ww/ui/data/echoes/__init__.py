from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QCompleter, QProgressBar, QTableWidgetItem

from ww.model.echoes import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.model.element import ElementEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echoes import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QDraggableTableWidget

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


def get_echo_list() -> List[str]:
    return echo_list


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


class QEchoesTable(QDraggableTableWidget):
    def __init__(self):
        echoes_table = EchoesTable()

        data = echoes_table.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        self._init_combobox()
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoesEnum.ID.value,
            column_names=echoes_table.df.columns,
        )

    def _init_column_width(self):
        col = self.column_names_table[EchoesEnum.ID.value]
        self.setColumnWidth(col, 400)

    def _init_combobox(self):
        self._echo_list = get_echo_list()
        self._elements = get_elements()
        self._echo_sonatas = get_echo_sonatas()

    def get_row_id(self, row: int) -> str:
        _id = []

        _prefix_i = self.column_names_table[EchoesEnum.PREFIX.value]
        _prefix = self.data[row][_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _element_i = self.column_names_table[EchoesEnum.ELEMENT.value]
        _element = self.data[row][_element_i]
        if _element:
            _id.append(_element)

        _name_i = self.column_names_table[EchoesEnum.NAME.value]
        _name = self.data[row][_name_i]
        if _name:
            _id.append(_name)

        _suffix_i = self.column_names_table[EchoesEnum.SUFFIX.value]
        _suffix = self.data[row][_suffix_i]
        if _suffix:
            _id.append(_suffix)

        id = " ".join(_id)
        return id

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == EchoesEnum.NAME.value:
            self.set_combobox(
                row,
                col,
                value,
                self._echo_list,
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
