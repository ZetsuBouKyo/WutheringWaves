import sys
from functools import partial
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QCompleter,
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

from ww.model.echo_skill import EchoSkillEnum
from ww.model.monsters import MonstersEnum
from ww.model.resonator_skill import (
    ResonatorSkillBaseAttrEnum,
    ResonatorSkillBonusTypeEnum,
    ResonatorSkillEnum,
)
from ww.model.resonators import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorsEnum,
    ResonatorsEnum,
)
from ww.model.template import CalculatedTemplateEnum, TemplateEnum
from ww.tables.echo_skill import EchoSkillTable
from ww.tables.monsters import MonstersTable
from ww.tables.resonator_skill import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.ui.combobox import QCustomComboBox
from ww.utils.number import get_number, get_string


def get_resonator_names() -> List[str]:
    resonators_table = ResonatorsTable()
    names = [name for name in resonators_table.df[ResonatorsEnum.ID].to_list() if name]
    return names


def get_resonator_skills(name: str) -> List[str]: ...


class QDamageSimple(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self._init_base()
        self._combobox_resonator_ids = self._init_combobox_resonator_ids()
        self._combobox_monster_ids = self._init_combobox_monster_ids()

        self.setLayout(self.layout)

    def _init_base(self):
        self._echo_skill_table = EchoSkillTable()
        self._monsters_table = MonstersTable()
        self._calculated_template_columns = [e.value for e in CalculatedTemplateEnum]

    def _init_combobox(self, label_name: str, getOptions, currentTextChanged):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)

        label = QLabel(label_name)
        label.setFixedWidth(100)
        layout.addWidget(label)

        combobox = QCustomComboBox(getOptions=getOptions)
        combobox.setFixedWidth(600)
        combobox.currentTextChanged.connect(currentTextChanged)
        layout.addWidget(combobox)

        self.layout.addLayout(layout)

        return combobox

    def _init_combobox_resonator_ids(self):
        return self._init_combobox(
            "共鳴者", get_resonator_names, self._combobox_event_update_resonator
        )

    def _get_monster_ids(self):
        names = [
            name
            for name in self._monsters_table.df[MonstersEnum.NAME].to_list()
            if name
        ]
        return names

    def _combobox_event_update_resonator(self, resonator_id: str):
        if resonator_id == "":
            return

        self._resonator_id = resonator_id
        self._resonators_table = ResonatorsTable()
        self._calculated_resonators_table = CalculatedResonatorsTable()

        # TODO: resonator skill -> row

    def _init_combobox_monster_ids(self):
        return self._init_combobox(
            "怪物", self._get_monster_ids, self._combobox_event_update_resonator
        )

    def _combobox_event_update_resonator(self, monster_id: str):
        # TODO: monster name -> monster id
        if monster_id == "":
            return

        self._monster_id = monster_id
        self._monster_level = get_number(
            self._monsters_table.search(self._monster_id, MonstersEnum.LEVEL)
        )
        self._monster_def = get_number(
            self._monsters_table.search(self._monster_id, MonstersEnum.DEF)
        )
