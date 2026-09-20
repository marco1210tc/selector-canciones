import tkinter as tk
from tkinter import ttk, messagebox

from models.station_model import StationModel

class StationsView:

    def __init__(self, parent):
        self.station_model = StationModel()

        self.window = tk.Toplevel(parent)
        self.window.title("Estaciones")
        self.window.geometry("700x450")
        self.window.resizable(True, True)

        self.create_widgets()
        self.load_stations()

    def create_widgets(self):
        # Contenedor principal
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Tabla
        columns = ("id", "nombre", "activo")

        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("activo", text="Estado")

        self.tree.column("id", width=50)
        self.tree.column("nombre", width=300)
        self.tree.column("activo", width=100)

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

        scrollbar.pack(side="right", fill="y")

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        # Botones
        buttons_frame = ttk.Frame(self.window, padding=(10, 0, 10, 10))
        buttons_frame.pack(fill="x")

        ttk.Button(
            buttons_frame,
            text="Nueva",
            command=self.create_station
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Editar",
            command=self.edit_station
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Activar / Desactivar",
            command=self.toggle_station
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Actualizar",
            command=self.load_stations
        ).pack(side="right", padx=5)

    def load_stations(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        stations = self.station_model.get_all()

        for station in stations:
            estado = "Activa" if station["activo"] else "Inactiva"

            self.tree.insert(
                "",
                "end",
                values=(
                    station["id"],
                    station["nombre"],
                    estado
                )
            )

    def get_selected_station(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selección",
                "Selecciona una estación."
            )
            return None

        values = self.tree.item(selected[0], "values")

        return {
            "id": int(values[0]),
            "nombre": values[1],
            "activo": values[2] == "Activa"
        }

    def create_station(self):
        StationForm(
            self.window,
            title="Nueva estación",
            on_save=self.save_new_station
        )

    def save_new_station(self, nombre):
        self.station_model.create(nombre)
        self.load_stations()

    def edit_station(self):
        station = self.get_selected_station()

        if station is None:
            return

        StationForm(
            self.window,
            title="Editar estación",
            station=station,
            on_save=self.save_edited_station
        )

    def save_edited_station(self, station_id, nombre):
        self.station_model.update(
            station_id,
            nombre
        )

        self.load_stations()

    def toggle_station(self):
        station = self.get_selected_station()

        if station is None:
            return

        nuevo_estado = not station["activo"]

        self.station_model.set_active(
            station["id"],
            nuevo_estado
        )

        self.load_stations()


class StationForm:

    def __init__(
        self,
        parent,
        title,
        on_save,
        station=None
    ):
        self.on_save = on_save
        self.station = station

        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("350x220")
        self.window.resizable(False, False)

        frame = ttk.Frame(
            self.window,
            padding=20
        )

        frame.pack(fill="both", expand=True)

        # Nombre
        ttk.Label(
            frame,
            text="Nombre:"
        ).pack(anchor="w")

        self.name_entry = ttk.Entry(frame)
        self.name_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        # Orden
        ttk.Label(
            frame,
            text="Orden:"
        ).pack(anchor="w")

        self.order_entry = ttk.Entry(frame)
        self.order_entry.pack(
            fill="x",
            pady=(5, 15)
        )

        # Valores cuando editamos
        if station:
            self.name_entry.insert(
                0,
                station["nombre"]
            )

        # Guardar
        ttk.Button(
            frame,
            text="Guardar",
            command=self.save
        ).pack(pady=10)

    def save(self):
        nombre = self.name_entry.get().strip()
        orden_text = self.order_entry.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "El nombre es obligatorio."
            )
            return
        
        if self.station:
            self.on_save(
                self.station["id"],
                nombre
            )
        else:
            self.on_save(
                nombre
            )

        self.window.destroy()