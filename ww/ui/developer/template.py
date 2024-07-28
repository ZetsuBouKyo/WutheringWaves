import sys
from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QComboBox,
    QCompleter,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.model.echoes import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.model.element import ElementEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echoes import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable
from ww.ui.table import QDraggableTableWidget
from ww.model.template import Templ

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


def get_echo_list() -> List[str]:
    return echo_list


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


class QTemplateTabTable(QDraggableTableWidget):
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

    def load(self, id: str): ...

    def get_row_id(self, row: List[str]) -> str:
        _id = []

        _prefix_i = self.column_names_table[EchoesEnum.PREFIX.value]
        _prefix = row[_prefix_i]
        if _prefix:
            _id.append(_prefix)

        _element_i = self.column_names_table[EchoesEnum.ELEMENT.value]
        _element = row[_element_i]
        if _element:
            _id.append(_element)

        _name_i = self.column_names_table[EchoesEnum.NAME.value]
        _name = row[_name_i]
        if _name:
            _id.append(_name)

        _suffix_i = self.column_names_table[EchoesEnum.SUFFIX.value]
        _suffix = row[_suffix_i]
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


class QTemplateTab(QWidget):
    def __init__(self):
        super().__init__()
