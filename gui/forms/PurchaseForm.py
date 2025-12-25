import tkinter as tk
from tkinter import ttk


class PurchaseForm(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master

        labels = ['Date', 'Source', 'Brand', 'Feed', 'Cost', 'Item Size', 'Item Unit', 'Quantity']

        self.entries = [tk.Entry(self) for i in labels]

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=1)
            self.entries[i].grid(row=i, column=2)
            if i < len(labels) - 1:
                self.entries[i].bind('<Tab>', lambda e, nf=self.entries[i + 1]: self.focus_next(nf))
            else:
                self.entries[i].bind('<Tab>', lambda e, nf=self.entries[0]: self.focus_next(nf))

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()
