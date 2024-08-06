import sys
from functools import partial
from pathlib import Path

from PySide2 import QtGui
from PySide2.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.locale import ZhHantEnum, _
from ww.ui.calc import QCalcTabs
from ww.ui.data import QDataTabs
from ww.ui.developer import QDevTabs
from ww.ui.gacha import QGachaTabs
from ww.ui.home import QHomeTab
from ww.ui.resource import QResourceTab

ICON_PATH = "./cache/v1/icon.webp"


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

        home = QHomeTab()
        public_data_tabs = QDataTabs()
        dev_tabs = QDevTabs()
        calc_tabs = QCalcTabs()
        gacha_tab = QGachaTabs()
        resource = QResourceTab()

        tabs_widget.addTab(home, "關於")
        tabs_widget.addTab(public_data_tabs, "數據")
        tabs_widget.addTab(dev_tabs, "開發者")
        tabs_widget.addTab(calc_tabs, _(ZhHantEnum.CALCULATE))
        tabs_widget.addTab(gacha_tab, "抽卡分析")
        tabs_widget.addTab(resource, "資源規劃")

        self.setCentralWidget(tabs_widget)
        self.center()

    def center(self):
        qr = self.frameGeometry()  # Get the frame geometry
        cp = (
            QDesktopWidget().availableGeometry().center()
        )  # Get the center point of the screen
        qr.moveCenter(cp)  # Move the center of the window to the center point
        self.move(qr.topLeft())  # Move the top left of the window to the top left of qr
