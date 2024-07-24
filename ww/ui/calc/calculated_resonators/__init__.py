from ww.model.echoes import EchoListEnum
from ww.model.resonators import CalculatedResonatorsEnum
from ww.tables.echoes import EchoListTable
from ww.tables.resonators import CalculatedResonatorsTable
from ww.ui.table import QUneditableTable

echo_list_table = EchoListTable()
echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]


class QCalculatedResonatorsTable(QUneditableTable):
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
