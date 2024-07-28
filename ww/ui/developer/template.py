import sys
from functools import partial
from pathlib import Path
from typing import Dict, List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QComboBox,
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

from ww.crud.echo import get_echo_names, get_echo_sonatas
from ww.crud.resonator import (
    get_resonator_chains,
    get_resonator_inherent_skills,
    get_resonator_names,
)
from ww.crud.weapon import get_weapon_names, get_weapon_ranks
from ww.model.echoes import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.model.element import ElementEnum
from ww.model.template import TemplateResonatorModel, TemplateResonatorModelEnum
from ww.tables.calculated_resonators import calc
from ww.tables.echoes import ECHOES_PATH, EchoesTable, EchoListTable
from ww.tables.resonator import RESONATOR_HOME_PATH
from ww.tables.weapon import WEAPON_HOME_PATH
from ww.ui.combobox import QCustomComboBox
from ww.ui.data.echoes import QEchoesTable
from ww.ui.data.resonators import QResonatorsTable
from ww.ui.table import QDraggableTableWidget
from ww.utils.pd import get_df, get_empty_df

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


def get_echo_list() -> List[str]:
    return echo_list


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


class QTemplateTabResonatorTable(QTableWidget):
    def __init__(self, resonators: List[TemplateResonatorModel] = []):
        self.column_names = [e.value for e in TemplateResonatorModelEnum]
        self.column_names_table: Dict[str, int] = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }
        self.resonators = resonators
        if len(self.resonators) == 0:
            self.data = [["" for _ in range(len(self.column_names))] for _ in range(3)]

        rows = 3
        columns = len(self.column_names)

        super().__init__(rows, columns)
        self._init_cells()
        self.setHorizontalHeaderLabels(self.column_names)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

    def get_cell(self, row: int, col: int) -> str:
        item = self.item(row, col)
        cell = self.cellWidget(row, col)
        if item is not None:
            return item.text()
        elif type(cell) == QCustomComboBox:
            return cell.currentText()
        return ""

    def get_resonators(self) -> List[TemplateResonatorModel]:
        data = []
        for row in range(self.rowCount()):
            resonator = TemplateResonatorModel()
            for col in range(self.columnCount()):
                cell = self.get_cell(row, col)
                if (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_NAME.value
                    ]
                ):
                    resonator.resonator_name = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_CHAIN.value
                    ]
                ):
                    resonator.resonator_chain = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_WEAPON_NAME.value
                    ]
                ):
                    resonator.resonator_weapon_name = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_WEAPON_RANK.value
                    ]
                ):
                    resonator.resonator_weapon_rank = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_INHERENT_SKILL_1.value
                    ]
                ):
                    if cell != "":
                        resonator.resonator_inherent_skill_1 = bool(int(cell))
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_INHERENT_SKILL_2.value
                    ]
                ):
                    if cell != "":
                        resonator.resonator_inherent_skill_2 = bool(int(cell))
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_1.value
                    ]
                ):
                    resonator.resonator_echo_1 = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_1.value
                    ]
                ):
                    resonator.resonator_echo_sonata_1 = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_2.value
                    ]
                ):
                    resonator.resonator_echo_sonata_2 = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_3.value
                    ]
                ):
                    resonator.resonator_echo_sonata_3 = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_4.value
                    ]
                ):
                    resonator.resonator_echo_sonata_4 = cell
                elif (
                    col
                    == self.column_names_table[
                        TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_5.value
                    ]
                ):
                    resonator.resonator_echo_sonata_5 = cell

            data.append(resonator)
        return data

    def set_combobox(
        self,
        row: int,
        column: int,
        name: str,
        names: List[str],
        currentIndexChanged=None,
        getOptions=None,
    ):
        if getOptions is None:
            combobox = QCustomComboBox()
            combobox.addItems(names)
            combobox.setCurrentText(name)
            completer = QCompleter(combobox.model())
            combobox.setCompleter(completer)
        else:
            combobox = QCustomComboBox(getOptions=getOptions)
            combobox.setCurrentText(name)

        # combobox.setStyleSheet("QComboBox { border: 1px solid #d8d8d8; }")

        if currentIndexChanged is not None:
            combobox.currentIndexChanged.connect(
                partial(currentIndexChanged, row, column, names)
            )

        self.setCellWidget(row, column, combobox)

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == TemplateResonatorModelEnum.RESONATOR_NAME.value:
            self.set_combobox(row, col, value, [], getOptions=get_resonator_names)
        elif self.column_names[col] == TemplateResonatorModelEnum.RESONATOR_CHAIN.value:
            self.set_combobox(row, col, value, [], getOptions=get_resonator_chains)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_WEAPON_NAME.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_weapon_names)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_WEAPON_RANK.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_weapon_ranks)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_INHERENT_SKILL_1.value
        ):
            self.set_combobox(
                row, col, value, [], getOptions=get_resonator_inherent_skills
            )
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_INHERENT_SKILL_2.value
        ):
            self.set_combobox(
                row, col, value, [], getOptions=get_resonator_inherent_skills
            )
        elif (
            self.column_names[col] == TemplateResonatorModelEnum.RESONATOR_ECHO_1.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_names)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_1.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_sonatas)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_2.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_sonatas)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_3.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_sonatas)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_4.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_sonatas)
        elif (
            self.column_names[col]
            == TemplateResonatorModelEnum.RESONATOR_ECHO_SONATA_5.value
        ):
            self.set_combobox(row, col, value, [], getOptions=get_echo_sonatas)
        else:
            item = QTableWidgetItem(value)
            self.setItem(row, col, item)


class QTemplateTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_btns_layout = QHBoxLayout()
        self.q_save_btn = QPushButton("存檔")
        self.q_save_btn.clicked.connect(self.save)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_save_btn)

        self.q_template_id_label = QLabel("模板ID")
        self.q_template_ids = QCustomComboBox()
        self.q_template_ids.setFixedWidth(700)
        self.q_template_ids.setFixedHeight(40)

        self.q_resonator_label = QLabel("共鳴者")
        self.q_resonator_table = QTemplateTabResonatorTable()
        self.q_resonator_table.setFixedHeight(180)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_template_id_label)
        self.layout.addWidget(self.q_template_ids)
        self.layout.addWidget(self.q_resonator_label)
        self.layout.addWidget(self.q_resonator_table)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def save(self):
        print(self.q_resonator_table.get_resonators())
