from typing import List

from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.locale import ZhTwEnum, _
from ww.model.buff import ResonatorBuffEnum
from ww.tables.buff import ResonatorBuffTable, get_resonator_buff_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.ui.table.cell import set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_buff_source_combobox,
    set_buff_target_combobox,
    set_buff_type_combobox,
    set_element_combobox,
    set_resonator_name_combobox,
    set_skill_bonus_type_combobox,
)


class QPrivateDataResonatorBuffTable(QDraggableTableWidget):
    def __init__(self):
        table = ResonatorBuffTable()
        column_names = table.column_names
        df = table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=ResonatorBuffEnum.ID.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 400)

    def get_row_id(self, row: List[str]) -> str:
        col_resonator_name = self.get_column_id(ResonatorBuffEnum.NAME.value)
        resonator_name = row[col_resonator_name]
        if not resonator_name:
            resonator_name = _(ZhTwEnum.NONE.value)

        col_source = self.get_column_id(ResonatorBuffEnum.SOURCE.value)
        source = row[col_source]
        if not source:
            source = _(ZhTwEnum.NONE.value)

        col_suffix = self.get_column_id(ResonatorBuffEnum.SUFFIX.value)
        suffix = row[col_suffix]
        if not suffix:
            suffix = _(ZhTwEnum.NONE.value)

        col_type = self.get_column_id(ResonatorBuffEnum.TYPE.value)
        type_ = row[col_type]
        col_element = self.get_column_id(ResonatorBuffEnum.ELEMENT.value)
        element = row[col_element]
        col_skill_type = self.get_column_id(ResonatorBuffEnum.SKILL_TYPE.value)
        skill_type = row[col_skill_type]
        if type_:
            if not element:
                if not skill_type:
                    final_type = type_
                else:
                    final_type = skill_type
            elif not skill_type:
                final_type = element
            else:
                final_type = _(ZhTwEnum.NONE.value)
        else:
            final_type = _(ZhTwEnum.NONE.value)

        col_target = self.get_column_id(ResonatorBuffEnum.TARGET.value)
        target = row[col_target]
        if not target:
            target = _(ZhTwEnum.NONE.value)

        primary_key = f"[{final_type}-{target}]{resonator_name}-{source}-{suffix}"
        return primary_key

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == ResonatorBuffEnum.ID.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.NAME.value:
            set_resonator_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.SOURCE.value:
            set_buff_source_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.TYPE.value:
            set_buff_type_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.ELEMENT.value:
            set_element_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.SKILL_TYPE.value:
            set_skill_bonus_type_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.TARGET.value:
            set_buff_target_combobox(self, row, col, value)
        else:
            super().set_cell(row, col, value)


class QPrivateDataResonatorBuffTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataResonatorBuffTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_resonator_buff_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
