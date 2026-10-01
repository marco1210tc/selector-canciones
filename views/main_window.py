import tkinter as tk
from tkinter import ttk

from views.program_types_view import ProgramTypesView
from views.stations_view import StationsView


class MainWindow:

    def __init__(self, database):
        self.database = database

        self.root = tk.Tk()
        self.root.title("Organizador de Culto")
        self.root.geometry("500x350")

        self.create_widgets()

    def create_widgets(self):

        frame = ttk.Frame(
            self.root,
            padding=30
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Organizador de Culto",
            font=("Arial", 18)
        ).pack(
            pady=(20, 30)
        )

        ttk.Button(
            frame,
            text="Administrar estaciones",
            command=self.open_stations
        ).pack(
            ipadx=20,
            ipady=10,
            pady=5
        )

        ttk.Button(
            frame,
            text="Administrar tipos de programa",
            command=self.open_program_types
        ).pack(
            ipadx=20,
            ipady=10,
            pady=5
        )

    def open_stations(self):
        StationsView(self.root)

    def open_program_types(self):
        ProgramTypesView(self.root)

    def run(self):
        self.root.mainloop()
