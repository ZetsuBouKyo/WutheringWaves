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

from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable


class QDevTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs

        template_tab = QWidget()
        private_data_tab = QWidget()

        self.addTab(template_tab, "模板")
        self.addTab(private_data_tab, "內部數據")
