from PySide2.QtWidgets import QTabWidget

from ww.locale import ZhTwEnum, _
from ww.ui.developer.private_data.echo.echo_list import QPrivateDataEchoListTab
from ww.ui.developer.private_data.echo.skill import QPrivateDataEchoSkillTab


class QPrivateDataEchoTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        # Tabs
        self.q_echo_list = QPrivateDataEchoListTab()
        self.q_echo_skill = QPrivateDataEchoSkillTab()

        # self.addTab(self.q_echo_list, _(ZhTwEnum.TAB_ECHO_LIST))
        self.addTab(self.q_echo_skill, _(ZhTwEnum.TAB_ECHO_SKILL))
