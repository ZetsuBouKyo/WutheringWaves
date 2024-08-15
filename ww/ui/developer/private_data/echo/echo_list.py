from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.echo import EchoTsvColumnEnum
from ww.tables.echo import EchoListTable, get_echo_list_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


class QPrivateDataEchoListTable(QDraggableTableWidget):
    def __init__(self):
        echo_list_table = EchoListTable()
        column_names = echo_list_table.column_names
        df = echo_list_table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoTsvColumnEnum.PRIMARY_KEY.value,
            column_names=column_names,
        )


class QPrivateDataEchoListTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataEchoListTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_echo_list_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
