import sys
from functools import partial
from typing import List

import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QCompleter,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ww.calc.damage import get_row_damage
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


class QDamageCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
