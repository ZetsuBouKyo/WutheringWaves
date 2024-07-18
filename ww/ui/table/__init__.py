# from tkinter import END, Entry


# class Table:

#     def __init__(self, self.root, data):
#         rows = len(data)
#         columns = len(data[0])

#         # code for creating table
#         for i in range(rows):
#             for j in range(columns):
#                 cell = Entry(self.root, width=20, fg="black", font=("Arial", 12, "normal"))

#                 cell.grid(row=i, column=j, padx=2, pady=2)
#                 cell.insert(END, data[i][j])

from tkinter import BOTH, END, Button, Canvas, Entry, Frame, Scrollbar

# Create a frame for the self.canvas with non-zero row&column weights


class Table:
    def __init__(self, root, data):
        self.root = root
        self.frame_canvas = Frame(self.root)

        rows = len(data)
        columns = len(data[0])

        self.frame_canvas.grid(row=0, column=0, sticky="nw")
        # self.frame_canvas.grid_rowconfigure(0, weight=1)
        # self.frame_canvas.grid_columnconfigure(0, weight=1)
        # # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        # self.frame_canvas.grid_propagate(False)

        # Add a self.canvas in that frame
        self.canvas = Canvas(self.frame_canvas)
        self.canvas.grid(row=0, column=0, sticky="nw")
        self.frame_canvas.update()

        # Link a scrollbar to the self.canvas
        self.scrollbar_y = Scrollbar(
            self.frame_canvas, orient="vertical", command=self.canvas.yview
        )
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = Scrollbar(
            self.frame_canvas, orient="horizontal", command=self.canvas.xview
        )
        self.scrollbar_x.grid(row=1, column=0, columnspan=2, sticky="we")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Create a frame to contain the buttons
        self.frame_cells = Frame(self.canvas)
        self.frame_cells.pack(fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.frame_cells, anchor="nw")

        rows = len(data)
        columns = len(data[0])

        cells = [[None for _ in range(columns)] for _ in range(rows)]
        for i in range(0, rows):
            for j in range(0, columns):
                cell = Entry(self.frame_cells)
                cell.grid(row=i, column=j, sticky="news")
                cell.insert(END, data[i][j])
                cells[i][j] = cell

        self.canvas.update()
        self.scrollbar_y_width = self.scrollbar_y.winfo_width()
        self.scrollbar_x_height = self.scrollbar_x.winfo_height()

        columns_width = self.root.winfo_width() - self.scrollbar_y_width
        rows_height = self.root.winfo_height() - self.scrollbar_x_height
        print(columns_width, rows_height, self.scrollbar_y.winfo_width())

        self.canvas.config(width=columns_width, height=rows_height)

        # Set the self.canvas scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def resize(self):
        self.canvas.update()
        self.scrollbar_y_width = self.scrollbar_y.winfo_width()
        self.scrollbar_x_height = self.scrollbar_x.winfo_height()

        columns_width = self.root.winfo_width() - self.scrollbar_y_width
        rows_height = self.root.winfo_height() - self.scrollbar_x_height
        # print(columns_width, rows_height, self.scrollbar_y.winfo_width())

        self.canvas.config(width=columns_width, height=rows_height)
