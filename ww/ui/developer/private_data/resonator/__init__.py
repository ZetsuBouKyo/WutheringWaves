import sys
from functools import partial

from PySide2.QtWidgets import (
    QApplication,
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

from ww.crud.resonator import get_resonator_names
from ww.locale import ZhHantEnum, _
from ww.ui.combobox import QCustomComboBox


class QPrivateDataResonatorTabs(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.q_resonator_layout = QHBoxLayout()
        self.q_resonator_label = QLabel(_(ZhHantEnum.NAME))
        self.q_resonator_label.setFixedHeight(40)
        self.q_resonator_combobox = QCustomComboBox(getOptions=get_resonator_names)
        self.q_resonator_combobox.setFixedHeight(40)
        self.q_resonator_combobox.setFixedWidth(150)
        self.q_resonator_layout.addWidget(self.q_resonator_label)
        self.q_resonator_layout.addWidget(self.q_resonator_combobox)
        self.q_resonator_layout.addStretch()

        self.resonator_name = self.q_resonator_combobox.currentText()

        # Tabs
        self.q_tabs = self.load_tabs(self.resonator_name)

        self.layout.addLayout(self.q_resonator_layout)
        self.layout.addWidget(self.q_tabs)

        self.setLayout(self.layout)

    def load_tabs(self, resonator_name: str) -> QTabWidget:
        self.q_tabs = QTabWidget()
        self.q_attr_tab = QWidget()
        self.q_skill_tab = QWidget()

        self.q_tabs.addTab(self.q_attr_tab, _(ZhHantEnum.TAB_ATTR))
        self.q_tabs.addTab(self.q_skill_tab, _(ZhHantEnum.TAB_SKILL))
        return self.q_tabs
