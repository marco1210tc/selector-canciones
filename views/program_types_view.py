import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from database.models.program_type_model import ProgramType


class ProgramTypesView:

    def __init__(self, parent):
        self.program_type_model = ProgramType()

        self.window = tk.Toplevel(parent)
        self.window.title("Tipos de programa")
        self.window.geometry("700x450")
        self.window.resizable(True, True)

        self.create_widgets()
        self.load_program_types()

    def create_widgets(self):

        # Contenedor principal
        main_frame = ttk.Frame(
            self.window,
            padding=10
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # Tabla
        columns = ("id", "nombre", "activo")

        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "nombre",
            text="Nombre"
        )

        self.tree.heading(
            "activo",
            text="Estado"
        )

        self.tree.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "nombre",
            width=350
        )

        self.tree.column(
            "activo",
            width=100,
            anchor="center"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        # Botones
        buttons_frame = ttk.Frame(
            self.window,
            padding=(10, 0, 10, 10)
        )

        buttons_frame.pack(
            fill="x"
        )

        ttk.Button(
            buttons_frame,
            text="Nuevo",
            command=self.create_program_type
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Editar",
            command=self.edit_program_type
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Activar / Desactivar",
            command=self.toggle_program_type
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Actualizar",
            command=self.load_program_types
        ).pack(
            side="right",
            padx=5
        )

    def load_program_types(self):

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        program_types = self.program_type_model.get_all()

        for program_type in program_types:

            estado = (
                "Activo"
                if program_type["activo"]
                else "Inactivo"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    program_type["id"],
                    program_type["nombre"],
                    estado
                )
            )

    def get_selected_program_type(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selección",
                "Selecciona un tipo de programa."
            )
            return None

        values = self.tree.item(
            selected[0],
            "values"
        )

        return {
            "id": int(values[0]),
            "nombre": values[1],
            "activo": values[2] == "Activo"
        }

    def create_program_type(self):

        ProgramTypeForm(
            self.window,
            title="Nuevo tipo de programa",
            on_save=self.save_new_program_type
        )

    def save_new_program_type(self, nombre):

        try:
            self.program_type_model.create(nombre)

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Ya existe un tipo de programa con ese nombre."
            )
            return

        self.load_program_types()

    def edit_program_type(self):

        program_type = self.get_selected_program_type()

        if program_type is None:
            return

        ProgramTypeForm(
            self.window,
            title="Editar tipo de programa",
            program_type=program_type,
            on_save=self.save_edited_program_type
        )

    def save_edited_program_type(
        self,
        program_type_id,
        nombre
    ):

        try:
            self.program_type_model.update(
                program_type_id,
                nombre
            )

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Ya existe un tipo de programa con ese nombre."
            )
            return

        self.load_program_types()

    def toggle_program_type(self):

        program_type = self.get_selected_program_type()

        if program_type is None:
            return

        nuevo_estado = not program_type["activo"]

        self.program_type_model.set_active(
            program_type["id"],
            nuevo_estado
        )

        self.load_program_types()


class ProgramTypeForm:

    def __init__(
        self,
        parent,
        title,
        on_save,
        program_type=None
    ):
        self.on_save = on_save
        self.program_type = program_type

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("380x180")
        self.window.resizable(False, False)

        frame = ttk.Frame(
            self.window,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        # Nombre
        ttk.Label(
            frame,
            text="Nombre:"
        ).pack(
            anchor="w"
        )

        self.name_entry = ttk.Entry(frame)

        self.name_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        # Valor cuando editamos
        if program_type:
            self.name_entry.insert(
                0,
                program_type["nombre"]
            )

        # Guardar
        ttk.Button(
            frame,
            text="Guardar",
            command=self.save
        ).pack(
            pady=10
        )

    def save(self):

        nombre = self.name_entry.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "El nombre es obligatorio."
            )
            return

        if self.program_type:

            self.on_save(
                self.program_type["id"],
                nombre
            )

        else:

            self.on_save(nombre)

        self.window.destroy()
