from tkinter import *
from tkinter import ttk


class MainView(ttk.Frame):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.best_btn = ttk.Button(self, text="Best")
        self.best_btn.grid(row=0, column=1, sticky="W")

        self.new_btn = ttk.Button(self, text="New")
        self.new_btn.grid(row=0, column=2, sticky="W")

        self.random_btn = ttk.Button(self, text="Random")
        self.random_btn.grid(row=0, column=3, sticky="W")

        self.text_field = Text()
        self.text_field.pack()

    def set_message(self, message: str) -> None:
        self.text_field.insert("1.0", f"{message}")
