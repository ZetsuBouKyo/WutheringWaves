from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.monsters import MonstersEnum
from ww.tables.monster import MonstersTable, get_monsters_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


class QPrivateDataMonsterTable(QDraggableTableWidget):
    def __init__(self):
        table = MonstersTable()
        column_names = table.column_names
        df = table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=MonstersEnum.NAME.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 400)


class QPrivateDataMonsterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataMonsterTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_monsters_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
