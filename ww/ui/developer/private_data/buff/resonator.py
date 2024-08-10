from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.buff import ResonatorBuffEnum
from ww.tables.buff import ResonatorBuffTable, get_resonator_buff_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.ui.table.cell.combobox import (
    set_buff_source_combobox,
    set_buff_target_combobox,
    set_buff_type_combobox,
    set_element_combobox,
    set_resonator_name_combobox,
    set_resonator_skill_bonus_type_combobox,
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

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == ResonatorBuffEnum.NAME.value:
            set_resonator_name_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.SOURCE.value:
            set_buff_source_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.TYPE.value:
            set_buff_type_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.ELEMENT.value:
            set_element_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffEnum.SKILL_TYPE.value:
            set_resonator_skill_bonus_type_combobox(self, row, col, value)
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
