from PySide2.QtWidgets import QTabWidget

from ww.locale import ZhTwEnum, _
from ww.ui.calc.calculated_resonators import QCalculatedResonators
from ww.ui.calc.resonator_compare import QResonatorDamageCompare
from ww.ui.calc.simple import QDamageSimple
from ww.ui.calc.team_compare import QTeamDamageCompare


class QCalcTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        calculated_resonators_tab = QCalculatedResonators()
        dmg_simple_tab = QDamageSimple()
        dmg_diff_resonator_tab = QResonatorDamageCompare()
        dmg_diff_team_tab = QTeamDamageCompare()

        self.addTab(calculated_resonators_tab, _(ZhTwEnum.TAB_RESONATOR))
        self.addTab(dmg_simple_tab, _(ZhTwEnum.TAB_SIMPLE_DAMAGE))
        self.addTab(dmg_diff_resonator_tab, _(ZhTwEnum.TAB_RESONATOR_DAMAGE_COMPARE))
        self.addTab(dmg_diff_team_tab, _(ZhTwEnum.TAB_TEAM_DAMAGE_COMPARE))
