from PySide2.QtWidgets import QTabWidget

from ww.locale import ZhHantEnum, _
from ww.ui.developer.private_data.buff.echo import QPrivateDataEchoBuffTab
from ww.ui.developer.private_data.buff.echo_sonata import QPrivateDataEchoSonataBuffTab
from ww.ui.developer.private_data.buff.resonator import QPrivateDataResonatorBuffTab
from ww.ui.developer.private_data.buff.weapon import QPrivateDataWeaponBuffTab


class QPrivateDataBuffTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_resonator = QPrivateDataResonatorBuffTab()
        self.q_weapon = QPrivateDataWeaponBuffTab()
        self.q_echo = QPrivateDataEchoBuffTab()
        self.q_echo_sonata = QPrivateDataEchoSonataBuffTab()

        self.addTab(self.q_resonator, _(ZhHantEnum.TAB_RESONATOR))
        self.addTab(self.q_weapon, _(ZhHantEnum.TAB_WEAPON))
        self.addTab(self.q_echo, _(ZhHantEnum.TAB_ECHO))
        self.addTab(self.q_echo_sonata, _(ZhHantEnum.TAB_ECHO_SONATA))
