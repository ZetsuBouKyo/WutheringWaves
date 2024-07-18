import tkinter as tk
from tkinter import BOTH, LEFT, Scrollbar, ttk

from ww.ui.table import Table

root_width = 100
root_height = 100

root = tk.Tk()
root.title("Wuthering Waves Damage calculator")
# root.geometry("1920x1080")
root.geometry(f"{root_width}x{root_height}")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(True, True)
root.update_idletasks()


# style = ttk.Style()
# style.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [4, 2]}}})
# style.theme_use("default")

tabs = ttk.Notebook(root)
tabs.grid(row=0, column=0, sticky="nw")

# calculated_resonators = ttk.Frame()
resonators = ttk.Frame(tabs)
resonators.grid(row=0, column=0, sticky="nw")
echoes = ttk.Frame(tabs)
templates = ttk.Frame(tabs)

tabs.add(resonators, text="共鳴者")
# tabs.add(calculated_resonators, text="[]")
tabs.add(echoes, text="聲骸")
tabs.add(templates, text="模板")

resonators.update_idletasks()

columns_width = resonators.winfo_width()
rows_height = resonators.winfo_height()
print(columns_width, rows_height)

# take the data
lst = [
    (1, "Raj", "Mumbai", 19),
    (2, "Aaryan", "Pune", 18),
    (3, "Vaishnavi", "Mumbai", 20),
    (4, "Rachna", "Mumbai", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (5, "Shubham", "Delhi", 21),
    (100, "Shubham", "Delhi", 21),
]


table = Table(resonators, lst)


class Cache:
    def __init__(self):
        self.last_width = root_width
        self.last_height = root_height
        self.lock = False


cache = Cache()
diff_sensitive = 100


def on_resize(event):
    if event.widget == event.widget.winfo_toplevel():
        print(dir(event))
        print(type(event))
        # current_width = event.width
        # current_height = event.height

        # width_diff = abs(current_width - cache.last_width)
        # height_diff = abs(current_height - cache.last_height)

        # if width_diff > diff_sensitive and height_diff > diff_sensitive:
        # table.resize()

        # cache.last_width = current_width
        # cache.last_height = current_height

        if cache.lock:
            return
        cache.lock = True
        table.resize()
        cache.lock = False


root.bind("<Configure>", on_resize)
