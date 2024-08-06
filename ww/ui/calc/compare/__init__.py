import sys
from decimal import Decimal
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

from ww.calc.damage import get_json_damage
from ww.locale import ZhHantEnum, _
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
from ww.tables.crud import get_row
from ww.tables.echo_skill import EchoSkillTable
from ww.tables.monsters import MonstersTable
from ww.tables.resonator_skill import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.ui.calc.compare.table import (
    QDamageCompareTable,
    QDamageCompareUneditableTable,
    QDamageCompareUneditableTableEnum,
)
from ww.ui.combobox import QCustomComboBox
from ww.utils.number import get_number, get_string


class QDamageCompare(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_damage_compare_table = QDamageCompareTable()
        self.q_damage_compare_uneditable_table = QDamageCompareUneditableTable()

        self.q_calculated_label = QLabel("計算結果")

        self.q_calculate_btn_layout = QHBoxLayout()
        self.q_calculate_btn = QPushButton(_(ZhHantEnum.CALCULATE))
        self.q_calculate_btn.clicked.connect(self.calculate)
        self.q_calculate_btn_layout.addStretch()
        self.q_calculate_btn_layout.addWidget(self.q_calculate_btn)

        self.layout.addLayout(self.q_calculate_btn_layout)
        self.layout.addWidget(self.q_damage_compare_table)
        self.layout.addWidget(self.q_calculated_label)
        self.layout.addWidget(self.q_damage_compare_uneditable_table)
        self.setLayout(self.layout)

    def calculate(self):
        data = []
        resonators_table = ResonatorsTable()
        damage_compare_table_data = self.q_damage_compare_table.get_current_data()
        for resonator_id, monster_id, template_id in damage_compare_table_data:
            damage = Decimal("0.0")
            damage_no_crit = Decimal("0.0")
            damage_crit = Decimal("0.0")

            resonator_name = resonators_table.search(resonator_id, ResonatorsEnum.NAME)
            rows = get_json_damage(template_id, monster_id, resonator_id, "", "")
            for row in rows:
                row_resonator_name = row.get(
                    CalculatedTemplateEnum.RESONATOR_NAME.value, None
                )
                if row_resonator_name != resonator_name:
                    continue
                row_damage = row.get(CalculatedTemplateEnum.DAMAGE.value, None)
                row_damage_no_crit = row.get(
                    CalculatedTemplateEnum.DAMAGE_NO_CRIT.value, None
                )
                row_damage_crit = row.get(
                    CalculatedTemplateEnum.DAMAGE_CRIT.value, None
                )

                damage += row_damage
                damage_no_crit += row_damage_no_crit
                damage_crit += row_damage_crit
                # print(row_damage, row_damage_no_crit, row_damage_crit)
            calculated_row = {
                QDamageCompareUneditableTableEnum.RESONATOR_ID.value: resonator_id,
                QDamageCompareUneditableTableEnum.MONSTER_ID.value: monster_id,
                QDamageCompareUneditableTableEnum.DAMAGE.value: str(damage),
                QDamageCompareUneditableTableEnum.DAMAGE_NO_CRIT.value: str(
                    damage_no_crit
                ),
                QDamageCompareUneditableTableEnum.DAMAGE_CRIT.value: str(damage_crit),
            }
            # print(calculated_row)
            data.append(calculated_row)
        self.q_damage_compare_uneditable_table.load_data(data)
