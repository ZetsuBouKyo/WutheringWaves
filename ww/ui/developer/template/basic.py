from typing import Dict, List

from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ww.crud.monster import get_monster_ids
from ww.crud.resonator import get_resonator_ids
from ww.crud.template import get_template_ids
from ww.locale import ZhTwEnum, _
from ww.model.resonator import ResonatorTsvColumnEnum
from ww.model.template import (
    TemplateModel,
    TemplateResonatorModel,
    TemplateResonatorTableColumnEnum,
)
from ww.tables.resonator import ResonatorsTable
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table import QBaseTableWidget
from ww.ui.table.cell import set_item
from ww.ui.table.cell.combobox import (
    set_echo_affix_combobox,
    set_echo_cost_combobox,
    set_echo_name_combobox,
    set_echo_sonata_combobox,
    set_resonator_base_attr_combobox,
    set_resonator_chain_combobox,
    set_resonator_inherent_skill_combobox,
    set_resonator_name_combobox,
    set_resonator_skill_bonus_combobox,
    set_weapon_name_combobox,
    set_weapon_rank_combobox,
)


class QTemplateTabResonatorTable(QBaseTableWidget):
    def __init__(self, resonators: List[TemplateResonatorModel] = []):
        self.column_names = [e.value for e in TemplateResonatorTableColumnEnum]
        self.column_names_table: Dict[str, int] = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = 3
        columns = len(self.column_names)

        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(self.column_names)
        self.load(resonators)

    def _init_cells(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.data[row][col]
                self.set_cell(row, col, cell)

    def load(self, resonators: List[TemplateResonatorModel]):
        self.resonators = resonators
        if len(self.resonators) == 0:
            self.data = [["" for _ in range(len(self.column_names))] for _ in range(3)]
        else:
            self.data = []
            for resonator in resonators:
                self.data.append(resonator.get_row())

        self._init_cells()

    def reset_data(self):
        self.setRowCount(0)
        self.setRowCount(3)
        self.data = self.get_empty_data(row_count=3)
        self._init_cells()

    def get_column_id(self, col_name: str) -> int:
        return self.column_names_table[col_name]

    def get_resonators(self) -> List[TemplateResonatorModel]:
        data = []
        for row in range(self.rowCount()):
            resonator = TemplateResonatorModel()
            for col in range(self.columnCount()):
                cell = self.get_cell(row, col)
                if col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_NAME.value
                ):
                    resonator.resonator_name = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_CHAIN.value
                ):
                    resonator.resonator_chain = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_WEAPON_NAME.value
                ):
                    resonator.resonator_weapon_name = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_WEAPON_RANK.value
                ):
                    resonator.resonator_weapon_rank = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_INHERENT_SKILL_1.value
                ):
                    if cell == "1":
                        resonator.resonator_inherent_skill_1 = True
                    elif cell == "0":
                        resonator.resonator_inherent_skill_1 = False
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_INHERENT_SKILL_2.value
                ):
                    if cell == "1":
                        resonator.resonator_inherent_skill_2 = True
                    elif cell == "0":
                        resonator.resonator_inherent_skill_2 = False
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_BASE_ATTR.value
                ):
                    resonator.resonator_base_attr = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_SKILL_BONUS.value
                ):
                    resonator.resonator_skill_bonus = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ENERGY_REGEN.value
                ):
                    resonator.resonator_energy_regen = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_1.value
                ):
                    resonator.resonator_echo_1 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_1.value
                ):
                    resonator.resonator_echo_sonata_1 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_2.value
                ):
                    resonator.resonator_echo_sonata_2 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_3.value
                ):
                    resonator.resonator_echo_sonata_3 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_4.value
                ):
                    resonator.resonator_echo_sonata_4 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_5.value
                ):
                    resonator.resonator_echo_sonata_5 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_1.value
                ):
                    resonator.resonator_echo_cost_1 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_2.value
                ):
                    resonator.resonator_echo_cost_2 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_3.value
                ):
                    resonator.resonator_echo_cost_3 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_4.value
                ):
                    resonator.resonator_echo_cost_4 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_5.value
                ):
                    resonator.resonator_echo_cost_5 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_1.value
                ):
                    resonator.resonator_echo_affix_1 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_2.value
                ):
                    resonator.resonator_echo_affix_2 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_3.value
                ):
                    resonator.resonator_echo_affix_3 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_4.value
                ):
                    resonator.resonator_echo_affix_4 = cell
                elif col == self.get_column_id(
                    TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_5.value
                ):
                    resonator.resonator_echo_affix_5 = cell

            data.append(resonator)
        return data

    def set_cell(self, row: int, col: int, value: str):
        if (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_NAME.value
        ):
            set_resonator_name_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_CHAIN.value
        ):
            set_resonator_chain_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_WEAPON_NAME.value
        ):
            set_weapon_name_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_WEAPON_RANK.value
        ):
            set_weapon_rank_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_INHERENT_SKILL_1.value
        ):
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_INHERENT_SKILL_2.value
        ):
            set_resonator_inherent_skill_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_BASE_ATTR.value
        ):
            set_resonator_base_attr_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_SKILL_BONUS.value
        ):
            set_resonator_skill_bonus_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_1.value
        ):
            set_echo_name_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_1.value
        ):
            set_echo_sonata_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_2.value
        ):
            set_echo_sonata_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_3.value
        ):
            set_echo_sonata_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_4.value
        ):
            set_echo_sonata_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_SONATA_5.value
        ):
            set_echo_sonata_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_1.value
        ):
            set_echo_cost_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_2.value
        ):
            set_echo_cost_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_3.value
        ):
            set_echo_cost_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_4.value
        ):
            set_echo_cost_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_COST_5.value
        ):
            set_echo_cost_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_1.value
        ):
            set_echo_affix_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_2.value
        ):
            set_echo_affix_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_3.value
        ):
            set_echo_affix_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_4.value
        ):
            set_echo_affix_combobox(self, row, col, value)
        elif (
            self.column_names[col]
            == TemplateResonatorTableColumnEnum.RESONATOR_ECHO_AFFIX_5.value
        ):
            set_echo_affix_combobox(self, row, col, value)
        else:
            set_item(self, row, col, value)


class QTemplateBasicTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        combobox_width = 900
        height = 40

        # Template ID
        self.q_template_id_layout = QHBoxLayout()
        self.q_template_id_label = QLabel(_(ZhTwEnum.ID))
        self.q_template_id_label.setFixedWidth(150)
        self.q_template_ids = QAutoCompleteComboBox(getOptions=get_template_ids)
        self.q_template_ids.setFixedWidth(combobox_width)
        self.q_template_ids.setFixedHeight(height)
        self.q_btns_layout = QHBoxLayout()
        self.q_get_template_id_btn = QPushButton(_(ZhTwEnum.DEFAULT_ID))
        self.q_get_template_id_btn.clicked.connect(self.create_template_id)
        self.q_get_template_id_btn.setFixedHeight(height)

        self.q_template_id_layout.addWidget(self.q_template_id_label)
        self.q_template_id_layout.addWidget(self.q_template_ids)
        self.q_template_id_layout.addStretch()
        self.q_template_id_layout.addWidget(self.q_get_template_id_btn)

        # Resonators 1
        self.q_test_resonator_1_layout = QHBoxLayout()
        self.q_test_resonator_1_label = QLabel("測試共鳴者1")
        self.q_test_resonator_1_label.setFixedWidth(150)
        self.q_test_resonator_1_combobox = QAutoCompleteComboBox(
            getOptions=get_resonator_ids
        )
        self.q_test_resonator_1_combobox.setFixedWidth(combobox_width)
        self.q_test_resonator_1_combobox.setFixedHeight(height)

        self.q_test_resonator_1_layout.addWidget(self.q_test_resonator_1_label)
        self.q_test_resonator_1_layout.addWidget(self.q_test_resonator_1_combobox)
        self.q_test_resonator_1_layout.addStretch()

        # Resonators 2
        self.q_test_resonator_2_layout = QHBoxLayout()
        self.q_test_resonator_2_label = QLabel("測試共鳴者2")
        self.q_test_resonator_2_label.setFixedWidth(150)
        self.q_test_resonator_2_combobox = QAutoCompleteComboBox(
            getOptions=get_resonator_ids
        )
        self.q_test_resonator_2_combobox.setFixedWidth(combobox_width)
        self.q_test_resonator_2_combobox.setFixedHeight(height)

        self.q_test_resonator_2_layout.addWidget(self.q_test_resonator_2_label)
        self.q_test_resonator_2_layout.addWidget(self.q_test_resonator_2_combobox)
        self.q_test_resonator_2_layout.addStretch()

        # Resonators 3
        self.q_test_resonator_3_layout = QHBoxLayout()
        self.q_test_resonator_3_label = QLabel("測試共鳴者3")
        self.q_test_resonator_3_label.setFixedWidth(150)
        self.q_test_resonator_3_combobox = QAutoCompleteComboBox(
            getOptions=get_resonator_ids
        )
        self.q_test_resonator_3_combobox.setFixedWidth(combobox_width)
        self.q_test_resonator_3_combobox.setFixedHeight(height)

        self.q_test_resonator_3_layout.addWidget(self.q_test_resonator_3_label)
        self.q_test_resonator_3_layout.addWidget(self.q_test_resonator_3_combobox)
        self.q_test_resonator_3_layout.addStretch()

        # Monster ID
        self.q_test_monster_id_layout = QHBoxLayout()
        self.q_test_monster_id_label = QLabel("測試怪物ID")
        self.q_test_monster_id_label.setFixedWidth(150)
        self.q_test_monster_id_combobox = QAutoCompleteComboBox(
            getOptions=get_monster_ids
        )
        self.q_test_monster_id_combobox.setFixedWidth(combobox_width)
        self.q_test_monster_id_combobox.setFixedHeight(height)

        self.q_test_monster_id_layout.addWidget(self.q_test_monster_id_label)
        self.q_test_monster_id_layout.addWidget(self.q_test_monster_id_combobox)
        self.q_test_monster_id_layout.addStretch()

        # Duration
        self.q_duration_layout = QHBoxLayout()
        self.q_duration_label = QLabel("時間")
        self.q_duration_label.setFixedWidth(150)
        self.q_duration_1_line = QLineEdit()
        self.q_duration_1_line.setFixedWidth(70)
        self.q_duration_1_line.setFixedHeight(height)
        self.q_duration_dash_label = QLabel("-")
        self.q_duration_dash_label.setFixedWidth(20)
        self.q_duration_2_line = QLineEdit()
        self.q_duration_2_line.setFixedWidth(70)
        self.q_duration_2_line.setFixedHeight(height)
        self.q_duration_layout.addWidget(self.q_duration_label)
        self.q_duration_layout.addWidget(self.q_duration_1_line)
        self.q_duration_layout.addWidget(self.q_duration_dash_label)
        self.q_duration_layout.addWidget(self.q_duration_2_line)
        self.q_duration_layout.addStretch()

        # Description
        self.q_description_label = QLabel("描述")
        self.q_description_label.setFixedHeight(height)
        self.q_description = QPlainTextEdit()
        self.q_description.setFixedHeight(120)

        # Table
        self.q_resonator_label = QLabel("共鳴者")
        self.q_resonator_label.setFixedHeight(height)
        self.q_resonator_table = QTemplateTabResonatorTable()
        self.q_resonator_table.setFixedHeight(200)

        self.layout.addLayout(self.q_template_id_layout)
        self.layout.addLayout(self.q_test_resonator_1_layout)
        self.layout.addLayout(self.q_test_resonator_2_layout)
        self.layout.addLayout(self.q_test_resonator_3_layout)
        self.layout.addLayout(self.q_test_monster_id_layout)
        self.layout.addLayout(self.q_duration_layout)
        self.layout.addWidget(self.q_description_label)
        self.layout.addWidget(self.q_description, 1)
        self.layout.addWidget(self.q_resonator_label)
        self.layout.addWidget(self.q_resonator_table)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def get_test_resonator_ids(self) -> List[str]:
        return [
            self.q_test_resonator_1_combobox.currentText(),
            self.q_test_resonator_2_combobox.currentText(),
            self.q_test_resonator_3_combobox.currentText(),
        ]

    def get_test_resonators(self) -> Dict[str, str]:
        table = {}
        resonators_table = ResonatorsTable()
        for resonator_id in self.get_test_resonator_ids():
            if not resonator_id:
                continue
            resonator_name = resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.NAME.value
            )
            if resonator_name is None:
                continue
            if table.get(resonator_name, None) is not None:
                QMessageBox.warning(self, _(ZhTwEnum.WARNING), "角色重複。")
                return table
            table[resonator_name] = resonator_id
        return table

    def get_monster_id(self) -> str:
        return self.q_test_monster_id_combobox.currentText()

    def get_duration_1(self) -> str:
        return self.q_duration_1_line.text()

    def get_duration_2(self) -> str:
        return self.q_duration_2_line.text()

    def get_description(self) -> str:
        return self.q_description.toPlainText()

    def get_resonators(self) -> List[TemplateResonatorModel]:
        return self.q_resonator_table.get_resonators()

    def get_template_id(self) -> str:
        return self.q_template_ids.currentText()

    def get_template(self) -> TemplateModel:
        template_id = self.get_template_id()
        template_id = template_id.strip()

        test_resonator_ids = self.get_test_resonator_ids()
        monster_id = self.get_monster_id()
        duration_1 = self.get_duration_1()
        duration_2 = self.get_duration_2()
        description = self.get_description()
        resonators = self.get_resonators()

        template = TemplateModel(
            id=template_id,
            test_resonator_id_1=test_resonator_ids[0],
            test_resonator_id_2=test_resonator_ids[1],
            test_resonator_id_3=test_resonator_ids[2],
            monster_id=monster_id,
            duration_1=duration_1,
            duration_2=duration_2,
            description=description,
            resonators=resonators,
        )

        return template

    def create_template_id(self):
        resonators = self.q_resonator_table.get_resonators()
        strs = []
        for resonator in resonators:
            resonator_chain = resonator.resonator_chain
            resonator_name = resonator.resonator_name
            weapon_rank = resonator.resonator_weapon_rank
            weapon_name = resonator.resonator_weapon_name
            if not resonator_name:
                continue

            if resonator_chain == "":
                resonator_chain = "0"
            if weapon_rank == "":
                weapon_rank = "1"

            r = f"+{resonator_chain}{resonator_name}"
            w = ""
            if weapon_name:
                w = f"+{weapon_rank}{weapon_name}"
            strs.append(r + w)
        id = ",".join(strs)
        if not id:
            return

        self.q_template_ids.setCurrentText(id)

    def reset_template_id(self) -> str:
        return self.q_template_ids.setCurrentText("")

    def load(self, template: TemplateModel):
        # Resonators
        self.q_test_resonator_1_combobox.setCurrentText(template.test_resonator_id_1)
        self.q_test_resonator_2_combobox.setCurrentText(template.test_resonator_id_2)
        self.q_test_resonator_3_combobox.setCurrentText(template.test_resonator_id_3)

        # Monster ID
        self.q_test_monster_id_combobox.setCurrentText(template.monster_id)

        # Duration
        self.q_duration_1_line.setText(template.duration_1)
        self.q_duration_2_line.setText(template.duration_2)

        # Description
        self.q_description.setPlainText(template.description)

        # Table
        self.q_resonator_table.load(template.resonators)

    def reset_data(self):
        self.q_template_ids.setCurrentText("")
        self.q_test_resonator_1_combobox.setCurrentText("")
        self.q_test_resonator_2_combobox.setCurrentText("")
        self.q_test_resonator_3_combobox.setCurrentText("")
        self.q_test_monster_id_combobox.setCurrentText("")
        self.q_duration_1_line.setText("")
        self.q_duration_2_line.setText("")
        self.q_description.setPlainText("")
        self.q_resonator_table.reset_data()
