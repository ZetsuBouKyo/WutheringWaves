import sys
from functools import partial
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
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

from ww.model.resonators import ResonatorsEnum
from ww.tables.resonators import ResonatorsTable
from ww.ui.combobox import QCustomComboBox


def get_resonator_names() -> List[str]:
    resonators_table = ResonatorsTable()
    names = resonators_table.df[ResonatorsEnum.ID].to_list()
    return names


def get_resonator_skills(name: str) -> List[str]: ...


class QDamageSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self._init_resonator_names()

        self.setLayout(self.layout)

    def _init_resonator_names(self):
        resonators_layout = QHBoxLayout()
        resonators_layout.setAlignment(Qt.AlignLeft)

        resonator_label = QLabel("共鳴者")
        resonators_layout.addWidget(resonator_label)

        self.resonator_names_combobox = QCustomComboBox(getOptions=get_resonator_names)
        self.resonator_names_combobox.setFixedWidth(400)
        resonators_layout.addWidget(self.resonator_names_combobox)

        self.layout.addLayout(resonators_layout)

    def _get_resonator_name(self) -> str:
        return self.resonator_names_combobox.currentText()

    def _init_resonator_skills(self): ...

    def _init_monsters(self): ...
