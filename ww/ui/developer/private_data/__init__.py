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


class QPrivateDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        q_resonator = QWidget()
        q_weapon = QWidget()
        q_echo = QWidget()
        q_buff = QWidget()

        self.addTab(q_resonator, "共鳴者")
        self.addTab(q_weapon, "武器")
        self.addTab(q_echo, "聲骸")
        self.addTab(q_buff, "增益")
