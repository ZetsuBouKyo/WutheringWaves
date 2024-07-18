from tkinter.ttk import Frame

from ww.tables.resonators import ResonatorsTable
from ww.ui.table import Table


class Resonators:
    def __init__(self, root, text: str):
        self.root = root
        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, sticky="nw")
        self.root.add(self.frame, text=text)

        resonators_table = ResonatorsTable()
        data = resonators_table.df.values.tolist()
        self.table = Table(self.frame, data)
