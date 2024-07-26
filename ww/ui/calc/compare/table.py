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
from ww.ui.table import QDraggableTableWidget, QUneditableTable
from ww.utils.pd import get_df, get_empty_df

DAMAGE_COMPARE_TABLE_HOME_PATH = "./cache/自訂/傷害比較"
DAMAGE_COMPARE_TABLE_CACHE_FNAME = "default.tsv"


class QDamageCompareTableEnum(str, Enum):
    ID: str = "角色代稱"
    MONSTER_ID: str = "怪物代稱"
    TEMPLATE_ID: str = "模板代稱"


class QDamageCompareTable(QDraggableTableWidget):
    def __init__(
        self,
        fname: str = DAMAGE_COMPARE_TABLE_CACHE_FNAME,
        progress: QProgressBar = None,
    ):
        tsv_path = Path(DAMAGE_COMPARE_TABLE_HOME_PATH) / fname
        column_names = [e.value for e in QDamageCompareTableEnum]
        if tsv_path.exists():
            self.df = get_df(tsv_path)
        else:
            self.df = get_empty_df(column_names)
        data = self.df.values.tolist()
        rows = len(data)
        columns = len(data[0])

        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=QDamageCompareTableEnum.ID.value,
            column_names=column_names,
            tsv_fpath=tsv_path,
            progress=progress,
        )

    def _init_column_width(self):
        for e in QDamageCompareTableEnum:
            col = self.column_names_table[e.value]
            self.setColumnWidth(col, 500)

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


class QDamageCompareUneditableTable(QUneditableTable):
    def __init__(self):
        calculated_resonators_table = CalculatedResonatorsTable()
        calculated_resonators_table_df = calculated_resonators_table.df
        super().__init__(calculated_resonators_table_df)

    def _init_column_width(self):
        for e in CalculatedResonatorsEnum:
            if e.value == CalculatedResonatorsEnum.ID.value:
                col = self.column_names_table[e.value]
                self.setColumnWidth(col, 500)
            else:
                width = len(e.value) * 20 + 50
                col = self.column_names_table[e.value]
                self.setColumnWidth(col, width)
