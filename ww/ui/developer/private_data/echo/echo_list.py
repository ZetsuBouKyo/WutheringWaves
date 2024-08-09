from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.echoes import EchoListEnum
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget
from ww.utils.pd import get_empty_df


class QPrivateDataEchoListTable(QDraggableTableWidget):
    def __init__(self):
        column_names = [e.value for e in EchoListEnum]
        df = get_empty_df(column_names)
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoListEnum.PRIMARY_KEY.value,
            column_names=column_names,
        )


class QPrivateDataEchoListTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataEchoListTable()
        self.q_tsv = QDraggableTsvTableWidget(self.q_table)
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
