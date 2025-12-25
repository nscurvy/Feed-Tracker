import tkinter as tk
from tkinter import ttk


class ConsumptionForm(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)

        labels = ['Date', 'Feed', 'Amount', 'Unit', 'Animal', 'Note[Optional]']

        self.entries = [tk.Entry(master=self) for i in labels]

        for i, label in enumerate(labels):
            tk.Label(master=self, text=label).grid(row=i, column=1)
            self.entries[i].grid(row=i, column=2)
            if i < len(labels) - 1:
                self.entries[i].bind('<Return>',
                                     lambda e, nf=self.entries[i + 1]: self.focus_next(nf))

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()
