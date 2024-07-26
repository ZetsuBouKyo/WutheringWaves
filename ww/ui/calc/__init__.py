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

from ww.ui.calc.calculated_resonators import QCalculatedResonators
from ww.ui.calc.compare import QDamageCompare
from ww.ui.calc.simple import QDamageSimple
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable


class QCalcTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        calculated_resonators_tab = QCalculatedResonators()
        dmg_simple_tab = QDamageSimple()
        dmg_diff_tab = QDamageCompare()
        dmg_detailed_tab = QWidget()

        self.addTab(calculated_resonators_tab, "共鳴者")
        self.addTab(dmg_simple_tab, "簡易傷害")
        self.addTab(dmg_diff_tab, "比較傷害")
        self.addTab(dmg_detailed_tab, "詳細傷害")
