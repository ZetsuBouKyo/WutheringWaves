from PySide2.QtWidgets import QVBoxLayout, QWidget

from ww.model.echo import EchoSkillEnum
from ww.tables.echo import EchoSkillTable, get_echo_skill_fpath
from ww.ui.table import QDraggableTableWidget, QDraggableTsvTableWidget


class QPrivateDataEchoSkillTable(QDraggableTableWidget):
    def __init__(self):
        echo_list_table = EchoSkillTable()
        column_names = echo_list_table.column_names
        df = echo_list_table.df
        data = df.values.tolist()
        rows = len(data)
        columns = len(column_names)
        super().__init__(
            rows,
            columns,
            data=data,
            column_id_name=EchoSkillEnum.PRIMARY_KEY.value,
            column_names=column_names,
        )


class QPrivateDataEchoSkillTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_table = QPrivateDataEchoSkillTable()
        self.q_tsv = QDraggableTsvTableWidget(
            self.q_table, tsv_fpath=get_echo_skill_fpath()
        )
        self.layout.addWidget(self.q_tsv)

        self.setLayout(self.layout)
