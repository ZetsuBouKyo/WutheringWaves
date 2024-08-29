from enum import Enum
from pathlib import Path

from ww.crud.template import get_template_label_names
from ww.locale import ZhTwEnum, _
from ww.ui.table import QDraggableTableWidget, QUneditableDataFrameTable
from ww.ui.table.cell.combobox import (
    set_combobox,
    set_monster_primary_key_combobox,
    set_resonator_primary_key_combobox,
    set_template_primary_key_combobox,
)
from ww.utils.pd import get_empty_df, safe_get_df

RESONATOR_DAMAGE_COMPARE_1_TABLE_HOME_PATH = (
    "./cache/v1/zh_tw/custom/resonator_damage_compare"
)
RESONATOR_DAMAGE_COMPARE_1_TABLE_CACHE_FNAME = "default.tsv"


class QResonatorDamageCompareTableEnum(str, Enum):
    RESONATOR_ID_1: str = _(ZhTwEnum.RESONATOR_ID_1)
    MONSTER_ID: str = _(ZhTwEnum.MONSTER_ID)
    TEMPLATE_ID: str = _(ZhTwEnum.TEMPLATE_ID)
    LABEL: str = _(ZhTwEnum.LABEL)


class QResonatorDamageCompareTable(QDraggableTableWidget):

    def __init__(
        self,
        fname: str = RESONATOR_DAMAGE_COMPARE_1_TABLE_CACHE_FNAME,
    ):
        _path = Path(RESONATOR_DAMAGE_COMPARE_1_TABLE_HOME_PATH) / fname
        self.column_names = [e.value for e in QResonatorDamageCompareTableEnum]

        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(rows, columns, data=data, column_names=self.column_names)

    def _init_column_width(self):
        self.setColumnWidth(0, 600)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 600)
        self.setColumnWidth(3, 150)

    def get_label_names(self):
        row = self.get_selected_row()
        if row is None:
            return []

        col_template_id = self.get_column_id(
            QResonatorDamageCompareTableEnum.TEMPLATE_ID.value
        )

        template_id = self.get_cell(row, col_template_id)
        if not template_id:
            return []

        return get_template_label_names(template_id)

    def set_cell(self, row: int, col: int, value: str):
        if (
            self.column_names[col]
            == QResonatorDamageCompareTableEnum.RESONATOR_ID_1.value
        ):
            set_resonator_primary_key_combobox(self, row, col, value)
        elif (
            self.column_names[col] == QResonatorDamageCompareTableEnum.MONSTER_ID.value
        ):
            set_monster_primary_key_combobox(self, row, col, value)
        elif (
            self.column_names[col] == QResonatorDamageCompareTableEnum.TEMPLATE_ID.value
        ):
            set_template_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QResonatorDamageCompareTableEnum.LABEL.value:
            set_combobox(self, row, col, value, [], getOptions=self.get_label_names)


class QResonatorDamageCompareUneditableTableEnum(str, Enum):
    RESONATOR_ID: str = "[角色]代稱"
    # RESONATOR_LEVEL: str = "[角色]等級"
    # RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    # RESONATOR_NAME: str = "[角色]名稱"
    # WEAPON_LEVEL: str = "[武器]等級"
    # WEAPON_RANK: str = "[武器]諧振"
    # WEAPON_NAME: str = "[武器]名稱"
    TEMPLATE_ID: str = _(ZhTwEnum.TEMPLATE_ID)
    LABEL: str = _(ZhTwEnum.LABEL)
    MONSTER_ID: str = "[怪物]名稱"
    DAMAGE: str = _(ZhTwEnum.RESULT_DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhTwEnum.RESULT_DAMAGE_CRIT)

    DAMAGE_DISTRIBUTION_BASIC: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_BASIC)
    DAMAGE_DISTRIBUTION_HEAVY: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_HEAVY)
    DAMAGE_DISTRIBUTION_SKILL: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_SKILL)
    DAMAGE_DISTRIBUTION_LIBERATION: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_LIBERATION)
    DAMAGE_DISTRIBUTION_INTRO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_INTRO)
    DAMAGE_DISTRIBUTION_OUTRO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_OUTRO)
    DAMAGE_DISTRIBUTION_ECHO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_ECHO)
    DAMAGE_DISTRIBUTION_NONE: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_NONE)


class QResonatorDamageCompareUneditableTable(QUneditableDataFrameTable):
    def __init__(self):
        column_names = [e.value for e in QResonatorDamageCompareUneditableTableEnum]
        self.df = get_empty_df(column_names)
        super().__init__(self.df)

    def reset_data(self):
        self.setRowCount(0)
        self.setRowCount(1)
        self.data = self.get_empty_data()
        self._init_cells()
