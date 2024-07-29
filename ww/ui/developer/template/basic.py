from typing import Dict, List

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTableWidgetItem,
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
from ww.model.template import TemplateResonatorModel, TemplateResonatorModelEnum
from ww.ui.combobox import QCustomComboBox
from ww.ui.table import QCustomTableWidget


class QTemplateTabResonatorTable(QCustomTableWidget):
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
        self.setHorizontalHeaderLabels(self.column_names)
        self._init_cells()

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(cell, row, col)

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


class QTemplateBasicTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_template_id_layout = QHBoxLayout()
        self.q_template_id_label = QLabel("模板ID")
        self.q_template_ids = QCustomComboBox()
        self.q_template_ids.setFixedWidth(700)
        self.q_template_ids.setFixedHeight(40)
        self.q_btns_layout = QHBoxLayout()
        self.q_get_template_id_btn = QPushButton("預設模板ID")
        self.q_get_template_id_btn.clicked.connect(self.get_template_id)
        self.q_get_template_id_btn.setFixedHeight(40)

        self.q_template_id_layout.addWidget(self.q_template_id_label)
        self.q_template_id_layout.addWidget(self.q_template_ids)
        self.q_template_id_layout.addStretch()
        self.q_template_id_layout.addWidget(self.q_get_template_id_btn)

        self.q_description_label = QLabel("描述")
        self.q_description = QPlainTextEdit()
        self.q_description.setFixedHeight(120)

        self.q_resonator_label = QLabel("共鳴者")
        self.q_resonator_table = QTemplateTabResonatorTable()
        self.q_resonator_table.setFixedHeight(180)

        self.layout.addLayout(self.q_template_id_layout)
        self.layout.addWidget(self.q_description_label)
        self.layout.addWidget(self.q_description)
        self.layout.addWidget(self.q_resonator_label)
        self.layout.addWidget(self.q_resonator_table)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def get_template_id(self): ...
