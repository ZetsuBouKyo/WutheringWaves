import tkinter as tk
from tkinter import BOTH, LEFT, Scrollbar, ttk

from ww.ui.resonators import Resonators
from ww.ui.table import Table

root_width = 1920
root_height = 1080

root = tk.Tk()
root.title("Wuthering Waves Damage calculator")
root.geometry(f"{root_width}x{root_height}")
root.resizable(True, True)
root.update_idletasks()

# style = ttk.Style()
# style.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [4, 2]}}})
# style.theme_use("default")

tabs = ttk.Notebook(root)
tabs.grid(row=0, column=0, sticky="nw")


# calculated_resonators = ttk.Frame()
resonators = Resonators(tabs, "共鳴者")

echoes = ttk.Frame(tabs)
templates = ttk.Frame(tabs)

# tabs.add(calculated_resonators, text="[]")
tabs.add(echoes, text="聲骸")
tabs.add(templates, text="模板")

tabs.update_idletasks()
tabs_height = tabs.winfo_height()
tabs_container_height = root_height - tabs_height

resonators.table.resize(root_width, 1000)
