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

from ww.locale import ZhHantEnum, _
from ww.ui.developer.private_data.resonator import QPrivateDataResonatorTabs
from ww.ui.developer.private_data.weapon import QPrivateDataWeaponTabs


class QPrivateDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_resonator = QPrivateDataResonatorTabs()
        self.q_weapon = QPrivateDataWeaponTabs()
        self.q_echo = QWidget()
        self.q_buff = QWidget()

        self.addTab(self.q_resonator, _(ZhHantEnum.RESONATOR))
        self.addTab(self.q_weapon, _(ZhHantEnum.WEAPON))
        self.addTab(self.q_echo, _(ZhHantEnum.ECHO))
        self.addTab(self.q_buff, _(ZhHantEnum.BUFF))
