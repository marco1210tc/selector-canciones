import tkinter as tk
from tkinter import ttk, messagebox

from database.models.station_model import StationModel
from database.models.program_type_station_model import ProgramTypeStationModel


class ProgramTypeStationView:

    def __init__(self, parent, program_type):
        self.parent = parent
        self.program_type = program_type

        self.program_type_station_model = ProgramTypeStationModel()
        self.station_model = StationModel()

        # Lista temporal de IDs de estaciones
        self.station_ids = []

        self.window = tk.Toplevel(parent)
        self.window.title(
            f"Estaciones - {program_type['nombre']}"
        )
        self.window.geometry("700x500")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_configuration()

    def create_widgets(self):

        # =========================
        # Encabezado
        # =========================

        header = ttk.Frame(
            self.window,
            padding=(20, 15)
        )
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Configuración de estaciones",
            font=("Arial", 16)
        ).pack(anchor="w")

        ttk.Label(
            header,
            text=f"Tipo de programa: {self.program_type['nombre']}"
        ).pack(anchor="w", pady=(5, 0))

        # =========================
        # Contenido
        # =========================

        content = ttk.Frame(
            self.window,
            padding=(20, 5, 20, 10)
        )
        content.pack(
            fill="both",
            expand=True
        )

        # =========================
        # Lista
        # =========================

        list_frame = ttk.LabelFrame(
            content,
            text="Estaciones del programa",
            padding=10
        )
        list_frame.pack(
            fill="both",
            expand=True
        )

        columns = ("orden", "nombre")

        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.tree.heading(
            "orden",
            text="Orden"
        )

        self.tree.heading(
            "nombre",
            text="Estación"
        )

        self.tree.column(
            "orden",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "nombre",
            width=400
        )

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =========================
        # Botones de orden
        # =========================

        order_frame = ttk.Frame(
            content
        )
        order_frame.pack(
            fill="x",
            pady=(8, 0)
        )

        ttk.Button(
            order_frame,
            text="Subir",
            command=self.move_up
        ).pack(
            side="left",
            padx=(0, 5)
        )

        ttk.Button(
            order_frame,
            text="Bajar",
            command=self.move_down
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            order_frame,
            text="Quitar",
            command=self.remove_station
        ).pack(
            side="left",
            padx=5
        )

        # =========================
        # Agregar estación
        # =========================

        add_frame = ttk.Frame(
            content
        )
        add_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        ttk.Label(
            add_frame,
            text="Agregar estación:"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.station_var = tk.StringVar()

        self.station_combo = ttk.Combobox(
            add_frame,
            textvariable=self.station_var,
            state="readonly",
            width=35
        )

        self.station_combo.pack(
            side="left"
        )

        ttk.Button(
            add_frame,
            text="Agregar",
            command=self.add_station
        ).pack(
            side="left",
            padx=10
        )

        # =========================
        # Footer
        # =========================

        bottom_frame = ttk.Frame(
            self.window,
            padding=(20, 10, 20, 15)
        )
        bottom_frame.pack(
            fill="x",
            side="bottom"
        )

        ttk.Button(
            bottom_frame,
            text="Guardar configuración",
            command=self.save_configuration
        ).pack(
            side="right",
            padx=(5, 0)
        )

        ttk.Button(
            bottom_frame,
            text="Cancelar",
            command=self.window.destroy
        ).pack(
            side="right"
        )

    # ==========================================================
    # Cargar configuración
    # ==========================================================

    def load_configuration(self):

        rows = self.program_type_station_model.get_by_program_type(
            self.program_type["id"]
        )

        self.station_ids = [
            row["station_id"]
            for row in rows
        ]

        self.refresh_tree()
        self.load_available_stations()

    # ==========================================================
    # Actualizar Treeview
    # ==========================================================

    def refresh_tree(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for orden, station_id in enumerate(
            self.station_ids,
            start=1
        ):

            station = self.station_model.get_by_id(
                station_id
            )

            if station is None:
                continue

            self.tree.insert(
                "",
                "end",
                iid=str(station_id),
                values=(
                    orden,
                    station["nombre"]
                )
            )

    # ==========================================================
    # Estaciones disponibles
    # ==========================================================

    def load_available_stations(self):

        stations = self.station_model.get_all(
            active_only=True
        )

        available = []

        self.station_lookup = {}

        for station in stations:

            if station["id"] in self.station_ids:
                continue

            display_name = station["nombre"]

            available.append(display_name)

            self.station_lookup[display_name] = station["id"]

        self.station_combo["values"] = available

        if available:
            self.station_combo.current(0)
        else:
            self.station_var.set("")

    # ==========================================================
    # Obtener estación seleccionada
    # ==========================================================

    def get_selected_station_index(self):

        selection = self.tree.selection()

        if not selection:
            return None

        station_id = int(selection[0])

        try:
            return self.station_ids.index(station_id)
        except ValueError:
            return None

    # ==========================================================
    # Agregar
    # ==========================================================

    def add_station(self):

        station_name = self.station_var.get()

        if not station_name:
            messagebox.showwarning(
                "Agregar estación",
                "Seleccione una estación."
            )
            return

        station_id = self.station_lookup.get(
            station_name
        )

        if station_id is None:
            return

        if station_id in self.station_ids:
            messagebox.showwarning(
                "Agregar estación",
                "La estación ya pertenece al programa."
            )
            return

        self.station_ids.append(station_id)

        self.refresh_tree()
        self.load_available_stations()

        # Seleccionar la estación recién agregada
        self.tree.selection_set(str(station_id))
        self.tree.focus(str(station_id))

    # ==========================================================
    # Quitar
    # ==========================================================

    def remove_station(self):

        index = self.get_selected_station_index()

        if index is None:
            messagebox.showwarning(
                "Quitar estación",
                "Seleccione una estación."
            )
            return

        station_id = self.station_ids[index]

        station = self.station_model.get_by_id(
            station_id
        )

        confirm = messagebox.askyesno(
            "Quitar estación",
            f"¿Desea quitar '{station['nombre']}' "
            "de este programa?"
        )

        if not confirm:
            return

        self.station_ids.pop(index)

        self.refresh_tree()
        self.load_available_stations()

    # ==========================================================
    # Subir
    # ==========================================================

    def move_up(self):

        index = self.get_selected_station_index()

        if index is None:
            messagebox.showwarning(
                "Ordenar",
                "Seleccione una estación."
            )
            return

        if index == 0:
            return

        self.station_ids[index], self.station_ids[index - 1] = (
            self.station_ids[index - 1],
            self.station_ids[index]
        )

        self.refresh_tree()

        new_station_id = self.station_ids[index - 1]

        self.tree.selection_set(
            str(new_station_id)
        )

        self.tree.focus(
            str(new_station_id)
        )

    # ==========================================================
    # Bajar
    # ==========================================================

    def move_down(self):

        index = self.get_selected_station_index()

        if index is None:
            messagebox.showwarning(
                "Ordenar",
                "Seleccione una estación."
            )
            return

        if index == len(self.station_ids) - 1:
            return

        self.station_ids[index], self.station_ids[index + 1] = (
            self.station_ids[index + 1],
            self.station_ids[index]
        )

        self.refresh_tree()

        new_station_id = self.station_ids[index + 1]

        self.tree.selection_set(
            str(new_station_id)
        )

        self.tree.focus(
            str(new_station_id)
        )

    # ==========================================================
    # Guardar
    # ==========================================================

    def save_configuration(self):

        try:

            self.program_type_station_model.save_configuration(
                self.program_type["id"],
                self.station_ids
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo guardar la configuración:\n\n{error}"
            )

            return

        messagebox.showinfo(
            "Configuración guardada",
            "La configuración de estaciones se guardó correctamente."
        )

        self.window.destroy()