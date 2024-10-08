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

from ww.ui.developer.private_data import QPrivateDataTabs
from ww.ui.developer.template import QTemplateTabs


class QDevTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        q_template_tab = QTemplateTabs()
        q_private_data_tab = QPrivateDataTabs()

        self.addTab(q_template_tab, "模板")
        self.addTab(q_private_data_tab, "內部數據")
