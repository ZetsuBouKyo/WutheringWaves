import sys
from functools import partial
from pathlib import Path

from PySide2 import QtGui
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.ui.calc import QCalcTabs
from ww.ui.data import QDataTabs

ICON_PATH = "./cache/icon.webp"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wuthering Waves Calculator")
        self.setGeometry(100, 100, 1920, 1080)

        icon_path = Path(ICON_PATH)
        if icon_path.exists():
            self.setWindowIcon(QtGui.QIcon(str(icon_path)))

        # Tabs
        tabs_widget = QTabWidget()

        public_data_tabs = QDataTabs()
        dev_tabs = QWidget()
        calc_tabs = QCalcTabs()

        tabs_widget.addTab(public_data_tabs, "數據")
        tabs_widget.addTab(dev_tabs, "開發者")
        tabs_widget.addTab(calc_tabs, "計算")

        self.setCentralWidget(tabs_widget)
