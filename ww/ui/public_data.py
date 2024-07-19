import sys
from functools import partial

from PySide2.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.ui.resonators import QResonatorsTable


def delete_selected_row(table):
    selected_row = table.currentRow()

    if selected_row != -1:
        table.removeRow(selected_row)


def get_public_data_tabs():
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
    resonators_tab_toolbar_layout = QHBoxLayout()
    # Create delete row button
    q_resonators_table = QResonatorsTable()
    delete_row_button = QPushButton("Delete Selected Row")
    delete_row_button.clicked.connect(partial(delete_selected_row, q_resonators_table))
    resonators_tab_toolbar_layout.addWidget(delete_row_button)
    resonators_tab_layout.addLayout(resonators_tab_toolbar_layout)
    resonators_tab_layout.addWidget(q_resonators_table)
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

    return tabs_widget
