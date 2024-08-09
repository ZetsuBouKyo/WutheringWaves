from PySide2.QtWidgets import QTabWidget, QWidget

from ww.locale import ZhHantEnum, _


class QPrivateDataEchoTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_echo_list = QWidget()
        self.q_echo_skill = QWidget()

        self.addTab(self.q_echo_list, _(ZhHantEnum.TAB_ECHO_LIST))
        self.addTab(self.q_echo_skill, _(ZhHantEnum.TAB_ECHO_SKILL))
