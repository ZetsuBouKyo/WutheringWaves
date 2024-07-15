import tkinter as tk
from tkinter import ttk

from ww.ui.resonators import resonators

root = tk.Tk()
root.title("Wuthering Waves Damage calculator")
root.geometry("1920x1080")

# style = ttk.Style()
# style.theme_settings("default", {"TNotebook.Tab": {"configure": {"padding": [4, 2]}}})
# style.theme_use("default")

tabs = ttk.Notebook(root)


# calculated_resonators = ttk.Frame()
echoes = ttk.Frame()
templates = ttk.Frame()

tabs.add(resonators, text="共鳴者")
# tabs.add(calculated_resonators, text="[]")
tabs.add(echoes, text="聲骸")
tabs.add(templates, text="模板")
tabs.pack(expand=1, fill="both")
