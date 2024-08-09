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
from ww.tables.echo import ECHOES_PATH
from ww.tables.resonators import RESONATORS_PATH
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable
from ww.ui.table import QDraggableTsvTableWidget


class QDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Resonators
        self.q_resonators_table = QResonatorsTable()

        # Echoes
        self.q_echoes_table = QEchoesTable()

        # Tabs
        resonators_tab = QDraggableTsvTableWidget(
            self.q_resonators_table,
            tsv_fpath=RESONATORS_PATH,
            event_save_after=calc,
        )
        echoes_tab = QDraggableTsvTableWidget(
            self.q_echoes_table,
            tsv_fpath=ECHOES_PATH,
            event_save_after=calc,
            event_save_row_before=self.q_echoes_table.set_row_cost,
        )

        self.addTab(resonators_tab, "共鳴者")
        self.addTab(echoes_tab, "聲骸")
