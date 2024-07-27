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

from ww.tables.calculated_resonators import calc
from ww.tables.echoes import ECHOES_PATH
from ww.tables.resonators import RESONATORS_PATH
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable
from ww.ui.table import QDraggableDataTableWidget


class QDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Resonators
        q_resonators_table = QResonatorsTable()
        q_echoes_table = QEchoesTable()

        # Echoes

        # Tabs
        resonators_tab = QDraggableDataTableWidget(
            q_resonators_table, tsv_fpath=RESONATORS_PATH, event_save=calc
        )
        echoes_tab = QDraggableDataTableWidget(
            q_echoes_table, tsv_fpath=ECHOES_PATH, event_save=calc
        )

        self.addTab(resonators_tab, "共鳴者")
        self.addTab(echoes_tab, "聲骸")
