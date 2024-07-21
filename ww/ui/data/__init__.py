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


class QDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        resonators_tab = QWidget()
        echoes_tab = QWidget()

        self.addTab(resonators_tab, "共鳴者")
        self.addTab(echoes_tab, "聲骸")

        # Resonators
        resonators_tab_layout = QVBoxLayout()
        resonators_tab_toolbar_layout = QHBoxLayout()

        q_resonators_progress_bar = QProgressBar()
        q_resonators_progress_bar.setMinimum(0)
        q_resonators_progress_bar.setMaximum(100)
        q_resonators_table = QResonatorsTable(progress=q_resonators_progress_bar)
        q_resonators_table_save_btn = QPushButton("Save")
        q_resonators_table_save_btn.clicked.connect(q_resonators_table.save)
        q_resonators_progress_bar_layout = QHBoxLayout()
        q_resonators_progress_bar_layout.addStretch()
        q_resonators_progress_bar_layout.addWidget(q_resonators_progress_bar)
        resonators_tab_toolbar_layout.addWidget(q_resonators_table_save_btn)
        resonators_tab_layout.addLayout(resonators_tab_toolbar_layout)
        resonators_tab_layout.addWidget(q_resonators_table)
        resonators_tab_layout.addLayout(q_resonators_progress_bar_layout)
        resonators_tab.setLayout(resonators_tab_layout)

        # Echoes
        echoes_tab_layout = QVBoxLayout()
        echoes_tab_toolbar_layout = QHBoxLayout()

        q_echoes_progress_bar = QProgressBar()
        q_echoes_progress_bar.setMinimum(0)
        q_echoes_progress_bar.setMaximum(100)
        q_echoes_table = QEchoesTable(progress=q_echoes_progress_bar)
        q_echoes_table_save_btn = QPushButton("Save")
        q_echoes_table_save_btn.clicked.connect(q_echoes_table.save)
        q_echoes_progress_bar_layout = QHBoxLayout()
        q_echoes_progress_bar_layout.addStretch()
        q_echoes_progress_bar_layout.addWidget(q_echoes_progress_bar)
        echoes_tab_toolbar_layout.addWidget(q_echoes_table_save_btn)
        echoes_tab_layout.addLayout(echoes_tab_toolbar_layout)
        echoes_tab_layout.addWidget(q_echoes_table)
        echoes_tab_layout.addLayout(q_echoes_progress_bar_layout)
        echoes_tab.setLayout(echoes_tab_layout)
