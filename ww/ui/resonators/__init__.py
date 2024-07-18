from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

from ww.tables.resonators import ResonatorsTable


class ResonatorsTableUI:
    def __init__(self):
        self.resonators_table = ResonatorsTable()
        data = self.resonators_table.df.values.tolist()

        column_names = self.resonators_table.df.columns

        rows = len(data)
        columns = len(data[0])

        self.table = QTableWidget(rows, columns)  # 5 rows and 3 columns
        self.table.setHorizontalHeaderLabels(column_names)

        # Fill the table with some data
        for row in range(rows):
            for col in range(columns):
                cell = data[row][col]
                item = QTableWidgetItem(cell)
                self.table.setItem(row, col, item)
