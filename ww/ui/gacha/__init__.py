import sys
from functools import partial
from pathlib import Path

from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
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

from ww.ui.gacha.base64 import QGachaBase64Tab
from ww.ui.gacha.file import QGachaFileTab
from ww.ui.gacha.url import QGachaUrlTab


class QGachaTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        # q_url_tab = QGachaUrlTab()
        q_file_tab = QGachaFileTab()
        q_base64_tab = QGachaBase64Tab()

        # self.addTab(q_url_tab, "網址")
        self.addTab(q_file_tab, "檔案")
        self.addTab(q_base64_tab, "base64")
