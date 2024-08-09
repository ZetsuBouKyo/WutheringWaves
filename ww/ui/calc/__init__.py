from PySide2.QtWidgets import QTabWidget

from ww.ui.calc.calculated_resonators import QCalculatedResonators
from ww.ui.calc.compare import QDamageCompare
from ww.ui.calc.simple import QDamageSimple


class QCalcTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        calculated_resonators_tab = QCalculatedResonators()
        dmg_simple_tab = QDamageSimple()
        dmg_diff_tab = QDamageCompare()

        self.addTab(calculated_resonators_tab, "共鳴者")
        self.addTab(dmg_simple_tab, "簡易傷害")
        self.addTab(dmg_diff_tab, "比較傷害")
