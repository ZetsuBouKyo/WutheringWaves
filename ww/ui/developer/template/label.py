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
    TemplateLabelModel,
    TemplateLabelTableColumnEnum,
    TemplateModel,
    TemplateResonatorModel,
    TemplateResonatorTableColumnEnum,
)
from ww.tables.resonator import ResonatorsTable
from ww.ui.combobox import QAutoCompleteComboBox
from ww.ui.table import QDraggableTableWidget
from ww.ui.table.cell import set_item
from ww.ui.table.cell.combobox import (
    set_echo_name_combobox,
    set_echo_sonata_combobox,
    set_resonator_chain_combobox,
    set_resonator_inherent_skill_combobox,
    set_resonator_name_combobox,
    set_weapon_name_combobox,
    set_weapon_rank_combobox,
)


class QTemplateLabelTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [e.value for e in TemplateLabelTableColumnEnum]
        self.column_names_table: Dict[str, int] = {
            column_names[i]: i for i in range(len(column_names))
        }
        rows = 0
        columns = len(column_names)

        super().__init__(rows, columns, column_names=column_names)

        self.setHorizontalHeaderLabels(self.column_names)
        self.load([])

    def load(self, labels: List[TemplateLabelModel]):
        if len(labels) == 0:
            self.data = self.get_empty_data()
        else:
            self.data = []
            for label in labels:
                self.data.append(label.get_row())

        self._init_cells()

    def get_labels(self) -> List[TemplateLabelModel]:
        labels = []
        for row in range(self.rowCount()):
            label = TemplateLabelModel()
            for col in range(self.columnCount()):
                cell = self.get_cell(row, col)
                if col == self.get_column_id(TemplateLabelTableColumnEnum.NAME.value):
                    label.name = cell
                elif col == self.get_column_id(
                    TemplateLabelTableColumnEnum.DURATION_1.value
                ):
                    label.duration_1 = cell
                elif col == self.get_column_id(
                    TemplateLabelTableColumnEnum.DURATION_2.value
                ):
                    label.duration_2 = cell
            labels.append(label)
        return labels

    def get_label_names(self) -> List[str]:
        labels = []
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell = self.get_cell(row, col)
                if col == self.get_column_id(TemplateLabelTableColumnEnum.NAME.value):
                    label_name = cell
                    labels.append(label_name)
        return labels

    def set_cell(self, row: int, col: int, value: str):
        set_item(self, row, col, value)


class QTemplateLabelTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.q_label_table = QTemplateLabelTable()
        self.layout.addWidget(self.q_label_table)
        self.setLayout(self.layout)

    def load(self, labels: List[TemplateLabelModel]):
        self.q_label_table.load(labels)

    def get_labels(self) -> List[TemplateLabelModel]:
        return self.q_label_table.get_labels()

    def get_label_names(self) -> List[str]:
        return self.q_label_table.get_label_names()

    def reset_data(self):
        self.q_label_table.reset_data()
