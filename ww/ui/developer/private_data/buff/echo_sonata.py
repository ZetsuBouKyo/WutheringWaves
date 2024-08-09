from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.buff import EchoSonataBuffEnum
from ww.tables.buff import EchoSonataBuffTable, get_echo_sonata_buff_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


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
            column_id_name=EchoSonataBuffEnum.ID.value,
            column_names=column_names,
        )

    def _init_column_width(self):
        self.setColumnWidth(0, 400)


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
