from PySide2.QtWidgets import QTableWidget, QTableWidgetItem

from ww.tables.resonators import ResonatorsTable


def get_resonators_table_ui():
    resonators_table = ResonatorsTable()
    data = resonators_table.df.values.tolist()

    column_names = resonators_table.df.columns

    rows = len(data)
    columns = len(data[0])

    table = QTableWidget(rows, columns)  # 5 rows and 3 columns
    table.setHorizontalHeaderLabels(column_names)

    for row in range(rows):
        for col in range(columns):
            cell = data[row][col]
            item = QTableWidgetItem(cell)
            table.setItem(row, col, item)
    return table
