from enum import Enum
from pathlib import Path

from ww.locale import ZhTwEnum, _
from ww.ui.table import QDraggableTableWidget, QUneditableDataFrameTable
from ww.ui.table.cell.combobox import (
    set_monster_primary_key_combobox,
    set_resonator_primary_key_combobox,
    set_template_primary_key_combobox,
)
from ww.utils.pd import get_empty_df, safe_get_df

DAMAGE_COMPARE_TABLE_HOME_PATH = "./cache/v1/custom/compare"
DAMAGE_COMPARE_TABLE_CACHE_FNAME = "default.tsv"


class QDamageCompareTableEnum(str, Enum):
    ID: str = "角色代稱"
    MONSTER_ID: str = "怪物代稱"
    TEMPLATE_ID: str = "模板代稱"


class QDamageCompareTable(QDraggableTableWidget):
    def __init__(
        self,
        fname: str = DAMAGE_COMPARE_TABLE_CACHE_FNAME,
    ):
        tsv_path = Path(DAMAGE_COMPARE_TABLE_HOME_PATH) / fname
        column_names = [e.value for e in QDamageCompareTableEnum]
        self.df = safe_get_df(tsv_path, column_names)

        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=QDamageCompareTableEnum.ID.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        for e in QDamageCompareTableEnum:
            col = self.get_column_id(e.value)
            self.setColumnWidth(col, 600)

    def _init_combobox(self):
        self._resonator_ids = None
        self._monster_ids = None
        self._template_ids = None

    def set_cell(self, row: int, col: int, value: str):
        if self.column_names[col] == QDamageCompareTableEnum.ID.value:
            set_resonator_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QDamageCompareTableEnum.MONSTER_ID.value:
            set_monster_primary_key_combobox(self, row, col, value)
        elif self.column_names[col] == QDamageCompareTableEnum.TEMPLATE_ID.value:
            set_template_primary_key_combobox(self, row, col, value)


class QDamageCompareUneditableTableEnum(str, Enum):
    RESONATOR_ID: str = "[角色]代稱"
    # RESONATOR_LEVEL: str = "[角色]等級"
    # RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    # RESONATOR_NAME: str = "[角色]名稱"
    # WEAPON_LEVEL: str = "[武器]等級"
    # WEAPON_RANK: str = "[武器]諧振"
    # WEAPON_NAME: str = "[武器]名稱"
    MONSTER_ID: str = "[怪物]名稱"
    DAMAGE: str = _(ZhTwEnum.DAMAGE)
    DAMAGE_NO_CRIT: str = _(ZhTwEnum.DAMAGE_NO_CRIT)
    DAMAGE_CRIT: str = _(ZhTwEnum.DAMAGE_CRIT)

    DAMAGE_DISTRIBUTION_BASIC: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_BASIC)
    DAMAGE_DISTRIBUTION_HEAVY: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_HEAVY)
    DAMAGE_DISTRIBUTION_SKILL: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_SKILL)
    DAMAGE_DISTRIBUTION_LIBERATION: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_LIBERATION)
    DAMAGE_DISTRIBUTION_INTRO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_INTRO)
    DAMAGE_DISTRIBUTION_OUTRO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_OUTRO)
    DAMAGE_DISTRIBUTION_ECHO: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_ECHO)
    DAMAGE_DISTRIBUTION_NONE: str = _(ZhTwEnum.DAMAGE_DISTRIBUTION_NONE)


class QDamageCompareUneditableTable(QUneditableDataFrameTable):
    def __init__(self):
        column_names = [e.value for e in QDamageCompareUneditableTableEnum]
        self.df = get_empty_df(column_names)
        super().__init__(self.df)
