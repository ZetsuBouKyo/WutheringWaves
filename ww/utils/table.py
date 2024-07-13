import pandas as pd
from rich.console import Console
from rich.table import Table


def print_table(title: str, df: pd.DataFrame):
    table = Table(title=title, show_header=True, header_style="bold magenta")
    console = Console()
    columns = []
    for column in df.columns:
        table.add_column(str(column))
        columns.append(column)

    for _, row in df.iterrows():
        _row = []
        for column in columns:
            _row.append(str(row[column]))
        table.add_row(*_row)

    console.print(table)


def print_transpose_table(title: str, df: pd.DataFrame):
    table = Table(title=title, show_header=True, header_style="bold magenta")
    console = Console()
    table.add_column("")
    columns = []
    for column in df.columns:
        table.add_column(str(column))
        columns.append(column)

    for _, row in df.iterrows():
        _row = [row.name]
        for column in columns:
            _row.append(str(row[column]))
        table.add_row(*_row)

    console.print(table)
