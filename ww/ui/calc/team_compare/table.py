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

TEAM_DAMAGE_COMPARE_TABLE_HOME_PATH = "./cache/v1/zh_tw/custom/team_damage_compare"
TEAM_DAMAGE_COMPARE_TABLE_CACHE_FNAME = "default.tsv"


class QTeamDamageCompareTableEnum(str, Enum):
    RESONATOR_ID_1: str = _(ZhTwEnum.RESONATOR_ID_1)
    RESONATOR_ID_2: str = _(ZhTwEnum.RESONATOR_ID_2)
    RESONATOR_ID_3: str = _(ZhTwEnum.RESONATOR_ID_3)
    MONSTER_ID: str = _(ZhTwEnum.MONSTER_ID)
    TEMPLATE_ID: str = _(ZhTwEnum.TEMPLATE_ID)


class QTeamDamageCompareTable(QDraggableTableWidget):

    def __init__(
        self,
        fname: str = TEAM_DAMAGE_COMPARE_TABLE_CACHE_FNAME,
    ):
        _path = Path(TEAM_DAMAGE_COMPARE_TABLE_HOME_PATH) / fname
        self.column_names = [e.value for e in QTeamDamageCompareTableEnum]

        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(rows, columns, data=data, column_names=self.column_names)

    def _init_column_width(self):
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 300)
        self.setColumnWidth(2, 300)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 500)

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


class QTeamDamageCompareUneditableTableEnum(str, Enum):
    RESONATOR_ID: str = "[角色]代稱"
    # RESONATOR_LEVEL: str = "[角色]等級"
    # RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    # RESONATOR_NAME: str = "[角色]名稱"
    # WEAPON_LEVEL: str = "[武器]等級"
    # WEAPON_RANK: str = "[武器]諧振"
    # WEAPON_NAME: str = "[武器]名稱"
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


class QTeamDamageCompareUneditableTable(QUneditableDataFrameTable):
    def __init__(self):
        column_names = [e.value for e in QTeamDamageCompareUneditableTableEnum]
        self.df = get_empty_df(column_names)
        super().__init__(self.df)
