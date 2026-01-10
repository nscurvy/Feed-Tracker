import tkinter as tk
from tkinter import ttk

from viewmodel import ProductViewModel


class ProductForm(ttk.Frame):
    def __init__(self, master, pvm: ProductViewModel):
        super().__init__(master)
        self.pvm = pvm
        labels = ['Feed', 'Animal Type', 'Source', 'Size', 'Unit', 'Brand', 'Cost', 'Update Date[Optional]']

        self.entries = {i: tk.Entry(self) for i in labels}

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=1)
            self.entries[label].grid(row=i, column=2)
            if i < len(labels) - 1:
                self.entries[label].bind('<Return>',
                                     lambda e, nf=self.entries[labels[i+1]]: self.focus_next(nf))
        self.submit_button = tk.Button(self, text='Submit', command=lambda entries=self.entries: self.submit_form(entries))
        self.submit_button.grid(row=len(labels), column=1)
        self.success_label = tk.Label(self)
        self.success_label.grid(row=len(labels) + 1, column=1)

    def focus_next(self, entry: tk.Entry) -> None:
        entry.focus_set()

    def submit_form(self, entries: dict[str, tk.Entry]) -> None:
        try:
            self.pvm.submit_product_form(
                feed=entries['Feed'].get(),
                animal_type=entries['Animal Type'].get(),
                source=entries['Source'].get(),
                size=entries['Size'].get(),
                unit=entries['Unit'].get(),
                brand=entries['Brand'].get(),
                cost=entries['Cost'].get(),
                update_date=entries['Update Date[Optional]'].get()
            )
            self.success_label['text'] = 'Successfully Submitted'
        except Exception as e:
            self.success_label['text'] = f'Error: {str(type(e))}: {str(e)}'
            raise e
