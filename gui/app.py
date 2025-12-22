import tkinter as tk
from tkinter import ttk

from .forms.ConsumptionForm import ConsumptionForm
from .forms.PurchaseForm import PurchaseForm


class FeedTrackerApp:
    def __init__(self, root: tk.Tk = None):
        self.root = root
        self.root.title("Feed Tracker")
        self.root.geometry("500x500")
        self.root.configure(background="gray")

        self.forms = {
            'Purchase': PurchaseForm(self.root),
            'Consumption': ConsumptionForm(self.root)
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


def run():
    root = tk.Tk()
    app = FeedTrackerApp(root)
    root.mainloop()