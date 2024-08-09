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

from ww.calc.damage import get_tsv_row_damage
from ww.model.echo import EchoListEnum, EchoSkillEnum
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
from ww.tables.echo import EchoListTable, EchoSkillTable
from ww.tables.monsters import MonstersTable
from ww.tables.resonator import ResonatorSkillTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.template import TemplateTable
from ww.ui.calc.compare.table import QDamageCompareTable, QDamageCompareUneditableTable
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QUneditableDataFrameTable
from ww.utils.number import get_number, get_string

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.PRIMARY_KEY] for _, row in echo_list_table.df.iterrows()]


class QCalculatedResonatorsTable(QUneditableDataFrameTable):
    def __init__(self):
        calculated_resonators_table = CalculatedResonatorsTable()
        calculated_resonators_table_df = calculated_resonators_table.df
        super().__init__(calculated_resonators_table_df)

    def _init_column_width(self):
        for e in CalculatedResonatorsEnum:
            if e.value == CalculatedResonatorsEnum.ID.value:
                col = self.get_column_id(e.value)
                self.setColumnWidth(col, 500)
            else:
                width = len(e.value) * 20 + 50
                col = self.get_column_id(e.value)
                self.setColumnWidth(col, width)

    def reload(self):
        calculated_resonators_table = CalculatedResonatorsTable()
        df = calculated_resonators_table.df
        self.data = df.values.tolist()
        self.column_names = df.columns
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = len(self.data)
        columns = len(self.data[0])
        self.setRowCount(rows)
        self.setColumnCount(columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_cells()
        self._init_column_width()


class QCalculatedResonators(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_calculated_resonators_table = QCalculatedResonatorsTable()

        self.q_calculated_label = QLabel("計算結果")

        self.q_btns_layout = QHBoxLayout()
        self.q_reload_btn = QPushButton("重新整理")
        self.q_reload_btn.clicked.connect(self.q_calculated_resonators_table.reload)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_reload_btn)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_calculated_resonators_table)
        self.setLayout(self.layout)
