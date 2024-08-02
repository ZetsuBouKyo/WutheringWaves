from enum import Enum
from functools import partial
from pathlib import Path

from PySide2.QtWidgets import QComboBox, QCompleter, QProgressBar

from ww.model.echoes import EchoListEnum
from ww.model.resonators import CalculatedResonatorsEnum
from ww.tables.crud import get_col
from ww.tables.echoes import EchoListTable
from ww.tables.monsters import MonstersEnum, MonstersTable
from ww.tables.resonators import CalculatedResonatorsTable, ResonatorsTable
from ww.tables.templates import get_template_ids
from ww.ui.table import QDraggableTableWidget, QUneditableDataFrameTable
from ww.utils.pd import get_empty_df, safe_get_df

DAMAGE_COMPARE_TABLE_HOME_PATH = "./cache/v1/自訂/傷害比較"
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

    def set_cell(self, value: str, row: int, col: int):
        if self.column_names[col] == QDamageCompareTableEnum.ID.value:
            self.set_combobox(
                row,
                col,
                value,
                [],
                getOptions=partial(
                    get_col, ResonatorsTable().df, QDamageCompareTableEnum.ID.value
                ),
            )
        elif self.column_names[col] == QDamageCompareTableEnum.MONSTER_ID.value:
            self.set_combobox(
                row,
                col,
                value,
                [],
                getOptions=partial(
                    get_col,
                    MonstersTable().df,
                    MonstersEnum.NAME.value,
                ),
            )
        elif self.column_names[col] == QDamageCompareTableEnum.TEMPLATE_ID.value:
            self.set_combobox(
                row,
                col,
                value,
                [],
                getOptions=get_template_ids,
            )


class QDamageCompareUneditableTableEnum(str, Enum):
    RESONATOR_ID: str = "[角色]代稱"
    # RESONATOR_LEVEL: str = "[角色]等級"
    # RESONATOR_CHAIN: str = "[角色]共鳴鏈"
    # RESONATOR_NAME: str = "[角色]名稱"
    # WEAPON_LEVEL: str = "[武器]等級"
    # WEAPON_RANK: str = "[武器]諧振"
    # WEAPON_NAME: str = "[武器]名稱"
    MONSTER_ID: str = "[怪物]名稱"
    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"


class QDamageCompareUneditableTable(QUneditableDataFrameTable):
    def __init__(self):
        column_names = [e.value for e in QDamageCompareUneditableTableEnum]
        self.df = get_empty_df(column_names)
        super().__init__(self.df)

    def _init_column_width(self): ...
