import tkinter as tk
from tkinter import ttk

from exception import InvalidFormSubmissionError
from viewmodel import PurchaseViewModel


class PurchaseForm(ttk.Frame):
    def __init__(self, master, pchvm: PurchaseViewModel):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.pchvm = pchvm

        labels = ['Date', 'Feed', 'Cost', 'Item Size', 'Item Unit', 'Source', 'Brand [Optional]',
                  'Quantity [Optional]']

        self.entries = {i: tk.Entry(self) for i in labels}

        animal_types = self.pchvm.get_animal_types()

        self.animal_selector = ttk.Combobox(self, values=animal_types, state='readonly')
        ttk.Label(self, text='Animal Type').grid(row=0, column=1)
        self.animal_selector.grid(row=0, column=2)

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i + 1, column=1)
            self.entries[label].grid(row=i+1, column=2)
            if i < len(labels) - 1:
                self.entries[label].bind('<Tab>', lambda e, nf=self.entries[labels[i + 1]]: self.focus_next(nf))
            else:
                self.entries[label].bind('<Tab>', lambda e, nf=self.entries[labels[0]]: self.focus_next(nf))
        self.submit_button = tk.Button(self, text='Submit', command=lambda entries=self.entries: self.submit_form(self.entries))
        self.submit_button.grid(row=len(labels) + 2, column=1)
        self.success_label = tk.Label(self)
        self.success_label.grid(row=len(labels) + 3, column=1)

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()

    def submit_form(self, entries: dict[str, tk.Entry]):
        try:
            self.pchvm.submit_form(
                purchase_date=entries['Date'].get(),
                feed=entries['Feed'].get(),
                animal_type=self.animal_selector.get(),
                cost=entries['Cost'].get(),
                item_size=entries['Item Size'].get(),
                item_unit=entries['Item Unit'].get(),
                source=entries['Source'].get(),
                brand=entries['Brand [Optional]'].get(),
                quantity=entries['Quantity [Optional]'].get(),
            )
        except InvalidFormSubmissionError as e:
            self.success_label['text'] = str(e)
