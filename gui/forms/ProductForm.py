import tkinter as tk
from tkinter import ttk


class ProductForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        labels = ['Feed', 'Source', 'Size', 'Unit', 'Brand', 'Cost']

        self.entries = [tk.Entry(self) for i in labels]

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=1)
            self.entries[i].grid(row=i, column=2)
            if i < len(labels) - 1:
                self.entries[i].bind('<Return>',
                                     lambda e, nf=self.entries[i + 1]: self.focus_next(nf))

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()
