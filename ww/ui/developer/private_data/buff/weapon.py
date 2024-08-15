from typing import List

from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.locale import ZhTwEnum, _
from ww.model.buff import ResonatorBuffTsvColumnEnum, WeaponBuffTsvColumnEnum
from ww.tables.buff import WeaponBuffTable, get_weapon_buff_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.ui.table.cell import set_uneditable_cell
from ww.ui.table.cell.combobox import (
    set_buff_type_combobox,
    set_element_combobox,
    set_skill_bonus_type_combobox,
    set_weapon_name_combobox,
    set_weapon_rank_combobox,
)


class QPrivateDataWeaponBuffTable(QDraggableTableWidget):
    def __init__(self):
        table = WeaponBuffTable()
        column_names = table.column_names
        df = table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=WeaponBuffTsvColumnEnum.ID.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 400)

    def get_row_id(self, row: List[str]) -> str:
        col_weapon_name = self.get_column_id(WeaponBuffTsvColumnEnum.NAME.value)
        weapon_name = row[col_weapon_name]
        if not weapon_name:
            weapon_name = _(ZhTwEnum.NONE.value)

        col_suffix = self.get_column_id(WeaponBuffTsvColumnEnum.SUFFIX.value)
        suffix = row[col_suffix]
        if not suffix:
            suffix = _(ZhTwEnum.NONE.value)

        col_rank = self.get_column_id(WeaponBuffTsvColumnEnum.RANK.value)
        rank = row[col_rank]
        if not rank:
            rank = _(ZhTwEnum.NONE.value)

        col_type = self.get_column_id(WeaponBuffTsvColumnEnum.TYPE.value)
        type_ = row[col_type]
        col_element = self.get_column_id(WeaponBuffTsvColumnEnum.ELEMENT.value)
        element = row[col_element]
        col_skill_type = self.get_column_id(WeaponBuffTsvColumnEnum.SKILL_TYPE.value)
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

        if suffix != _(ZhTwEnum.NONE.value):
            primary_key = (
                f"[{final_type}]{weapon_name}-{rank}{_(ZhTwEnum.TUNE)}-{suffix}"
            )
        else:
            primary_key = f"[{final_type}]{weapon_name}-{rank}{_(ZhTwEnum.TUNE)}"
        return primary_key

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == WeaponBuffTsvColumnEnum.ID.value:
            set_uneditable_cell(self, row, col, value)
        elif self.column_names[col] == WeaponBuffTsvColumnEnum.NAME.value:
            set_weapon_name_combobox(self, row, col, value)
        elif self.column_names[col] == WeaponBuffTsvColumnEnum.RANK.value:
            set_weapon_rank_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffTsvColumnEnum.TYPE.value:
            set_buff_type_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffTsvColumnEnum.ELEMENT.value:
            set_element_combobox(self, row, col, value)
        elif self.column_names[col] == ResonatorBuffTsvColumnEnum.SKILL_TYPE.value:
            set_skill_bonus_type_combobox(self, row, col, value)
        else:
            super().set_cell(row, col, value)


class QPrivateDataWeaponBuffTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataWeaponBuffTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_weapon_buff_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
