from typing import List

from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.locale import ZhTwEnum, _
from ww.model.buff import EchoSonataBuffTsvColumnEnum
from ww.tables.buff import EchoSonataBuffTable, get_echo_sonata_buff_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.ui.table.cell import set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_buff_target_combobox,
    set_buff_type_combobox,
    set_echo_sonata_combobox,
    set_element_combobox,
    set_skill_bonus_type_combobox,
)


class QPrivateDataEchoSonataBuffTable(QDraggableTableWidget):
    def __init__(self):
        table = EchoSonataBuffTable()
        column_names = table.column_names
        df = table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoSonataBuffTsvColumnEnum.ID.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 400)

    def get_row_id(self, row: List[str]) -> str:
        col_name = self.get_column_id(EchoSonataBuffTsvColumnEnum.NAME.value)
        name = row[col_name]
        if not name:
            name = _(ZhTwEnum.NONE.value)

        col_suffix = self.get_column_id(EchoSonataBuffTsvColumnEnum.SUFFIX.value)
        suffix = row[col_suffix]
        if not suffix:
            suffix = _(ZhTwEnum.NONE.value)

        col_type = self.get_column_id(EchoSonataBuffTsvColumnEnum.TYPE.value)
        type_ = row[col_type]
        col_element = self.get_column_id(EchoSonataBuffTsvColumnEnum.ELEMENT.value)
        element = row[col_element]
        col_skill_type = self.get_column_id(
            EchoSonataBuffTsvColumnEnum.SKILL_TYPE.value
        )
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

        col_target = self.get_column_id(EchoSonataBuffTsvColumnEnum.TARGET.value)
        target = row[col_target]
        if not target:
            target = _(ZhTwEnum.NONE.value)

        if suffix == _(ZhTwEnum.NONE.value):
            primary_key = f"[{final_type}-{target}]{name}"
        else:
            primary_key = f"[{final_type}-{target}]{name}-{suffix}"
        return primary_key

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == EchoSonataBuffTsvColumnEnum.ID.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == EchoSonataBuffTsvColumnEnum.NAME.value:
            set_echo_sonata_combobox(self, row, col, value)
        elif self.column_names[col] == EchoSonataBuffTsvColumnEnum.TYPE.value:
            set_buff_type_combobox(self, row, col, value)
        elif self.column_names[col] == EchoSonataBuffTsvColumnEnum.ELEMENT.value:
            set_element_combobox(self, row, col, value)
        elif self.column_names[col] == EchoSonataBuffTsvColumnEnum.SKILL_TYPE.value:
            set_skill_bonus_type_combobox(self, row, col, value)
        elif self.column_names[col] == EchoSonataBuffTsvColumnEnum.TARGET.value:
            set_buff_target_combobox(self, row, col, value)
        else:
            super().set_cell(row, col, value)


class QPrivateDataEchoSonataBuffTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataEchoSonataBuffTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_echo_sonata_buff_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
