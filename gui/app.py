import tkinter as tk
from tkinter import ttk
from sqlite3 import Connection

from .forms.ConsumptionForm import ConsumptionForm
from .forms.ProductForm import ProductForm
from .forms.PurchaseForm import PurchaseForm
from .forms.AnimalForm import AnimalForm

from viewmodel import AnimalViewModel, ProductViewModel


class FeedTrackerApp:
    def __init__(self, root: tk.Tk = None, conn: Connection = None):
        self.root = root
        self.root.title("Feed Tracker")
        self.root.geometry("500x500")
        self.root.configure(background="gray")

        avm = AnimalViewModel(conn)
        pvm = ProductViewModel(conn)

        self.forms = {
            'Log Purchase': PurchaseForm(self.root),
            'Log Consumption': ConsumptionForm(self.root),
            'Add Product': ProductForm(self.root, pvm),
            'Update Animal': AnimalForm(self.root, avm),
        }

        self.selector = ttk.Combobox(self.root, values=list(self.forms.keys()), state="readonly")
        self.selector.pack(pady=10)
        self.selector.bind('<<ComboboxSelected>>', self.show_form)

        self.current_form = None
        self.selector.current(0)
        self.show_form()

    def show_form(self, event=None):
        if self.current_form:
            self.current_form.pack_forget()

        form = self.forms[self.selector.get()]
        form.pack(fill='both', expand=True)
        self.current_form = form


def focus_next(entry: tk.Entry):
    entry.focus_set()


def execute():
    pass


def run(conn: Connection):
    root = tk.Tk()
    app = FeedTrackerApp(root, conn)
    root.mainloop()