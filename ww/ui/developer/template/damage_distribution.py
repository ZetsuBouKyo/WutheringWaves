from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.locale import ZhHantEnum, _


class QTemplateDamageDistributionTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.q_resonator_1 = QWidget()
        self.q_resonator_2 = QWidget()
        self.q_resonator_3 = QWidget()

        self.addTab(self.q_resonator_1, _(ZhHantEnum.RESONATOR_1))
        self.addTab(self.q_resonator_2, _(ZhHantEnum.RESONATOR_2))
        self.addTab(self.q_resonator_3, _(ZhHantEnum.RESONATOR_3))

    def calculate(self): ...
