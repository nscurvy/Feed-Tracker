from sqlite3 import Error
import tkinter as tk
from tkinter import ttk

from viewmodel import AnimalViewModel


class AnimalForm(ttk.Frame):
    def __init__(self, master: tk.Tk, viewmodel: AnimalViewModel) -> None:
        super().__init__(master)
        self.viewmodel = viewmodel

        labels = ['Animal Name', 'Population Change', 'Date of Change', 'Reason (Optional)']

        self.entries = {labels[i]: tk.Entry(master=self) for i in range(len(labels))}

        for i, label in enumerate(labels):
            tk.Label(master=self, text=label).grid(row=i, column=1)
            self.entries[label].grid(row=i, column=2)
            if i < len(labels) - 1:
                self.entries[label].bind('<Return>', lambda e, nf=
                tuple([i for i in self.entries.values()])[i + 1]: self.focus_next(nf))
        buttonrow = len(labels) + 1
        tk.Button(self, text='Submit', command=lambda: self.submit(self.entries)).grid(
            row=buttonrow, column=3)
        self.successlabel = tk.Label(self)
        self.successlabel.grid(row=buttonrow + 1, column=1)

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()

    def submit(self, values: dict[str, tk.Entry]) -> None:
        try:
            self.viewmodel.update_animal(animal_name=values['Animal Name'].get(),
                                         delta=values['Population Change'].get(),
                                         date_of_change=values['Date of Change'].get(),
                                         reason=values['Reason (Optional)'].get())
            self.successlabel['text'] = "Success!"
        except Error as error:
            self.successlabel['text'] = f'Error! {error.sqlite_errorname}'
