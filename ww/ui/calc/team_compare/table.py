from enum import Enum

from ww.crud.template import get_template_label_names
from ww.locale import ZhTwEnum, _
from ww.ui.table import QDraggableTableWidget, QUneditableDataFrameTable
from ww.ui.table.cell.combobox import (
    set_combobox,
    set_monster_primary_key_combobox,
    set_resonator_primary_key_combobox,
    set_template_primary_key_combobox,
)
from ww.utils.pd import get_empty_df


class QTeamDamageCompareTableEnum(str, Enum):
    RESONATOR_ID_1: str = _(ZhTwEnum.RESONATOR_ID_1)
    RESONATOR_ID_2: str = _(ZhTwEnum.RESONATOR_ID_2)
    RESONATOR_ID_3: str = _(ZhTwEnum.RESONATOR_ID_3)
    MONSTER_ID: str = _(ZhTwEnum.MONSTER_ID)
    TEMPLATE_ID: str = _(ZhTwEnum.TEMPLATE_ID)
    LABEL: str = _(ZhTwEnum.LABEL)


class QTeamDamageCompareTable(QDraggableTableWidget):

    def __init__(self):

        self.column_names = [e.value for e in QTeamDamageCompareTableEnum]

        self.df = get_empty_df(self.column_names)

        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(rows, columns, data=data, column_names=self.column_names)

    def _init_column_width(self):
        self.setColumnWidth(0, 600)
        self.setColumnWidth(1, 600)
        self.setColumnWidth(2, 600)
        self.setColumnWidth(3, 400)
        self.setColumnWidth(4, 600)
        self.setColumnWidth(5, 150)

    def get_label_names(self):
        row = self.get_selected_row()
        if row is None:
            return []

        col_template_id = self.get_column_id(
            QTeamDamageCompareTableEnum.TEMPLATE_ID.value
        )

        template_id = self.get_cell(row, col_template_id)
        if not template_id:
            return []

        return get_template_label_names(template_id)

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == QTeamDamageCompareTableEnum.RESONATOR_ID_1.value:
            set_resonator_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QTeamDamageCompareTableEnum.RESONATOR_ID_2.value:
            set_resonator_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QTeamDamageCompareTableEnum.RESONATOR_ID_3.value:
            set_resonator_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QTeamDamageCompareTableEnum.MONSTER_ID.value:
            set_monster_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QTeamDamageCompareTableEnum.TEMPLATE_ID.value:
            set_template_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QTeamDamageCompareTableEnum.LABEL.value:
            set_combobox(self, row, col, value, [], getOptions=self.get_label_names)


class QTeamDamageCompareUneditableTableEnum(str, Enum):
    TEMPLATE_ID: str = _(ZhTwEnum.TEMPLATE_ID)
    LABEL: str = _(ZhTwEnum.LABEL)
    MONSTER_ID: str = "[怪物]名稱"
    DURATION_1: str = _(ZhTwEnum.DURATION_1)
    DURATION_2: str = _(ZhTwEnum.DURATION_2)
    MIN_DPS: str = _(ZhTwEnum.RESULT_MIN_DPS)
    MAX_DPS: str = _(ZhTwEnum.RESULT_MAX_DPS)
    DAMAGE: str = _(ZhTwEnum.RESULT_DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_CRIT)


class QTeamDamageCompareUneditableTable(QUneditableDataFrameTable):
    def __init__(self):
        column_names = [e.value for e in QTeamDamageCompareUneditableTableEnum]
        self.df = get_empty_df(column_names)
        super().__init__(self.df)

    def _init_column_width(self):
        self.setColumnWidth(0, 600)

    def reset_data(self):
        self.setRowCount(0)
        self.setRowCount(1)
        self.data = self.get_empty_data()
        self._init_cells()
