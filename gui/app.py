import tkinter as tk
from tkinter import ttk


def focus_next(entry: tk.Entry):
    entry.focus_set()


def execute():
    pass


def run():
    root = tk.Tk()
    root.title("Test Form")
    root.geometry("500x500")
    root.configure(background="gray")

    labels = ['Date', 'Source', 'Brand', 'Feed', 'Cost', 'Size', 'Unit']
    entries = [tk.Entry(root) for i in labels]

    for i, label in enumerate(labels):
        tk.Label(root, text=label).grid(row=i, column=1)
        entries[i].grid(row=i, column=2)
        if i < len(labels) - 1:
            entries[i].bind('<Tab>', lambda e, nf=entries[i+1]: focus_next(nf))
        else:
            entries[i].bind('<Tab>', lambda e, nf=entries[0]: focus_next(nf))

    button = tk.Button(root, text="Run", command=execute)
    button.grid(row=len(labels) + 1, column=1)

    root.mainloop()
