from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ww.model.echo import EchoListEnum
from ww.model.resonator import CalculatedResonatorColumnEnum
from ww.tables.echo import EchoListTable
from ww.tables.resonator import CalculatedResonatorsTable
from ww.ui.table import QUneditableDataFrameTable

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.PRIMARY_KEY] for _, row in echo_list_table.df.iterrows()]


class QCalculatedResonatorsTable(QUneditableDataFrameTable):
    def __init__(self):
        calculated_resonators_table = CalculatedResonatorsTable()
        calculated_resonators_table_df = calculated_resonators_table.df
        super().__init__(calculated_resonators_table_df)

    def _init_column_width(self):
        for e in CalculatedResonatorColumnEnum:
            if e.value == CalculatedResonatorColumnEnum.ID.value:
                col = self.get_column_id(e.value)
                self.setColumnWidth(col, 500)
            else:
                width = len(e.value) * 20 + 50
                col = self.get_column_id(e.value)
                self.setColumnWidth(col, width)

    def reload(self):
        calculated_resonators_table = CalculatedResonatorsTable()
        df = calculated_resonators_table.df
        self.data = df.values.tolist()
        self.column_names = df.columns
        self.column_names_table = {
            self.column_names[i]: i for i in range(len(self.column_names))
        }

        rows = len(self.data)
        columns = len(self.data[0])
        self.setRowCount(rows)
        self.setColumnCount(columns)

        self.setHorizontalHeaderLabels(self.column_names)

        self._init_cells()
        self._init_column_width()


class QCalculatedResonators(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.q_calculated_resonators_table = QCalculatedResonatorsTable()

        self.q_calculated_label = QLabel("計算結果")

        self.q_btns_layout = QHBoxLayout()
        self.q_reload_btn = QPushButton("重新整理")
        self.q_reload_btn.clicked.connect(self.q_calculated_resonators_table.reload)
        self.q_btns_layout.addStretch()
        self.q_btns_layout.addWidget(self.q_reload_btn)

        self.layout.addLayout(self.q_btns_layout)
        self.layout.addWidget(self.q_calculated_resonators_table)
        self.setLayout(self.layout)
