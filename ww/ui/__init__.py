import sys

from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.ui.resonators import ResonatorsTableUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide2 Tab Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a QTabWidget
        tab_widget = QTabWidget()

        # Create tabs
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add tabs to the QTabWidget
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")
        tab_widget.addTab(tab3, "Tab 3")

        # Set up layout for tab 1
        tab1_layout = QVBoxLayout()
        tab1_label = QLabel("This is Tab 1")
        tab1_layout.addWidget(tab1_label)
        tab1.setLayout(tab1_layout)

        # Set up layout for tab 2
        tab2_layout = QVBoxLayout()
        tab2_label = QLabel("This is Tab 2")
        tab2_layout.addWidget(tab2_label)

        resonators_table_ui = ResonatorsTableUI()
        tab2_layout.addWidget(resonators_table_ui.table)
        tab2.setLayout(tab2_layout)

        # Set up layout for tab 3
        tab3_layout = QVBoxLayout()
        tab3_label = QLabel("This is Tab 3")
        tab3_layout.addWidget(tab3_label)
        tab3.setLayout(tab3_layout)

        # Set the central widget of the main window
        self.setCentralWidget(tab_widget)
