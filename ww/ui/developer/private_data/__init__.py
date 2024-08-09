from PySide2.QtWidgets import QTabWidget, QWidget

from ww.locale import ZhHantEnum, _
from ww.ui.developer.private_data.echo import QPrivateDataEchoTabs
from ww.ui.developer.private_data.resonator import QPrivateDataResonatorTabs
from ww.ui.developer.private_data.weapon import QPrivateDataWeaponTabs


class QPrivateDataTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_resonator = QPrivateDataResonatorTabs()
        self.q_weapon = QPrivateDataWeaponTabs()
        self.q_echo = QPrivateDataEchoTabs()
        self.q_buff = QWidget()

        self.addTab(self.q_resonator, _(ZhHantEnum.RESONATOR))
        self.addTab(self.q_weapon, _(ZhHantEnum.WEAPON))
        self.addTab(self.q_echo, _(ZhHantEnum.ECHO))
        self.addTab(self.q_buff, _(ZhHantEnum.BUFF))
