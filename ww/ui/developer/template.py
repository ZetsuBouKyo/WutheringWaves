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
from ww.model.template import TemplateResonatorModelEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echoes import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable
from ww.ui.table import QDraggableTableWidget
from ww.utils.pd import get_df, get_empty_df

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


def get_echo_list() -> List[str]:
    return echo_list


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


class QTemplateTabResonatorTable(QDraggableTableWidget):
    def __init__(self):
        tsv_path = ""
        column_names = [e.value for e in TemplateResonatorModelEnum]

        # TODO:
        # if tsv_path.exists():
        #     self.df = get_df(tsv_path)
        # else:
        #     self.df = get_empty_df(column_names)

        self.df = get_empty_df(column_names)

        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(
            rows,
            columns,
            data=data,
            column_names=column_names,
        )

    def _init_column_width(self): ...


class QTemplateTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_save_btn = QPushButton("存檔")
        # self.q_save_btn.clicked.connect()
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_save_btn)

        self.q_resonator_label = QLabel("共鳴者")
        self.q_resonator_table = QTemplateTabResonatorTable()
        self.q_resonator_table.setFixedHeight(180)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_resonator_label)
        self.layout.addWidget(self.q_resonator_table)
        self.layout.addStretch()
        self.setLayout(self.layout)
