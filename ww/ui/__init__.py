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

from ww.ui.resonators import get_resonators_table_ui


def delete_selected_row(table):
    selected_row = table.currentRow()

    if selected_row != -1:
        table.removeRow(selected_row)


def do_nothing():
    return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide2 Tab Example")
        self.setGeometry(100, 100, 1920, 1080)

        # Create a QTabWidget
        tabs_widget = QTabWidget()

        # Create tabs
        resonators_tab = QWidget()
        echo_tab = QWidget()
        template_tab = QWidget()

        # Add tabs to the QTabWidget
        tabs_widget.addTab(resonators_tab, "共鳴者")
        tabs_widget.addTab(echo_tab, "聲骸")
        tabs_widget.addTab(template_tab, "模板")

        # Set up layout for tab 1
        resonators_tab_layout = QVBoxLayout()
        # Create delete row button
        resonators_table_ui = get_resonators_table_ui()
        delete_row_button = QPushButton("Delete Selected Row")
        delete_row_button.clicked.connect(
            partial(delete_selected_row, resonators_table_ui)
        )
        resonators_tab_layout.addWidget(delete_row_button)
        resonators_tab_layout.addWidget(resonators_table_ui)
        resonators_tab.setLayout(resonators_tab_layout)

        # Set up layout for tab 2
        echo_layout = QVBoxLayout()
        tab2_label = QLabel("This is Tab 2")
        echo_layout.addWidget(tab2_label)

        echo_tab.setLayout(echo_layout)

        # Set up layout for tab 3
        template_layout = QVBoxLayout()
        tab3_label = QLabel("This is Tab 3")
        template_layout.addWidget(tab3_label)
        template_tab.setLayout(template_layout)

        # Set the central widget of the main window
        self.setCentralWidget(tabs_widget)
