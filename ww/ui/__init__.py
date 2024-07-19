import sys
from functools import partial

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

from ww.ui.public_data import get_public_data_tabs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wuthering Waves")
        self.setGeometry(100, 100, 1920, 1080)

        # Create a QTabWidget
        tabs_widget = QTabWidget()

        # Create tabs
        public_data_tabs = get_public_data_tabs()
        result_tabs = QWidget()

        # Add tabs to the QTabWidget
        tabs_widget.addTab(public_data_tabs, "數據")
        tabs_widget.addTab(result_tabs, "結果")

        # Set the central widget of the main window
        self.setCentralWidget(tabs_widget)
