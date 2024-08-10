from PySide2.QtWidgets import QTabWidget, QWidget

from ww.locale import ZhTwEnum, _
from ww.ui.developer.private_data.buff import QPrivateDataBuffTabs
from ww.ui.developer.private_data.echo import QPrivateDataEchoTabs
from ww.ui.developer.private_data.monster import QPrivateDataMonsterTab
from ww.ui.developer.private_data.resonator import QPrivateDataResonatorTabs
from ww.ui.developer.private_data.weapon import QPrivateDataWeaponTabs


class QPrivateDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_resonator = QPrivateDataResonatorTabs()
        self.q_weapon = QPrivateDataWeaponTabs()
        self.q_echo = QPrivateDataEchoTabs()
        self.q_monster = QPrivateDataMonsterTab()
        self.q_buff = QPrivateDataBuffTabs()

        self.addTab(self.q_resonator, _(ZhTwEnum.TAB_RESONATOR))
        self.addTab(self.q_weapon, _(ZhTwEnum.TAB_WEAPON))
        self.addTab(self.q_echo, _(ZhTwEnum.TAB_ECHO))
        self.addTab(self.q_monster, _(ZhTwEnum.TAB_MONSTER))
        self.addTab(self.q_buff, _(ZhTwEnum.TAB_BUFF))
