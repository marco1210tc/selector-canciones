import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from database.models.song_model import SongModel
from database.models.station_model import StationModel


class SongsView:

    def __init__(self, parent):

        self.parent = parent

        self.song_model = SongModel()
        self.station_model = StationModel()

        self.window = tk.Toplevel(parent)
        self.window.title("Administrar canciones")
        self.window.geometry("900x500")

        self.create_widgets()
        self.load_songs()

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def create_widgets(self):

        frame = ttk.Frame(
            self.window,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # Tabla
        # ------------------------------------------------------

        columns = (
            "id",
            "titulo",
            "tipo",
            "numero_himno",
            "referencia",
            "orden",
            "estacion",
            "activo"
        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "titulo": "Título",
            "tipo": "Tipo",
            "numero_himno": "N.º Himno",
            "referencia": "Referencia",
            "orden": "Orden",
            "estacion": "Estación",
            "activo": "Activo"
        }

        for column, heading in headings.items():
            self.tree.heading(
                column,
                text=heading
            )

        self.tree.column(
            "id",
            width=40,
            anchor="center"
        )

        self.tree.column(
            "titulo",
            width=250
        )

        self.tree.column(
            "tipo",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "numero_himno",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "referencia",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "orden",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "estacion",
            width=130
        )

        self.tree.column(
            "activo",
            width=60,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            frame,
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

        # ------------------------------------------------------
        # Botones
        # ------------------------------------------------------

        buttons_frame = ttk.Frame(
            self.window,
            padding=(20, 0, 20, 20)
        )

        buttons_frame.pack(
            fill="x"
        )

        ttk.Button(
            buttons_frame,
            text="Nueva",
            command=self.new_song
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Editar",
            command=self.edit_song
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Activar/Desactivar",
            command=self.toggle_active
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Actualizar",
            command=self.load_songs
        ).pack(
            side="right",
            padx=5
        )

    # ==========================================================
    # CARGAR
    # ==========================================================

    def load_songs(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        songs = self.song_model.get_all()

        for song in songs:

            numero = (
                song["numero_himno"]
                if song["numero_himno"] is not None
                else ""
            )

            activo = (
                "Sí"
                if song["activo"]
                else "No"
            )

            self.tree.insert(
                "",
                "end",
                iid=str(song["id"]),
                values=(
                    song["id"],
                    song["titulo"],
                    song["tipo"],
                    numero,
                    song["referencia"],
                    song["orden"],
                    song["station_name"],
                    activo
                )
            )

    # ==========================================================
    # SELECCIÓN
    # ==========================================================

    def get_selected_song(self):

        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Canciones",
                "Seleccione una canción."
            )
            return None

        song_id = int(selection[0])

        return self.song_model.get_by_id(song_id)

    # ==========================================================
    # NUEVA
    # ==========================================================

    def new_song(self):

        SongForm(
            self.window,
            self.station_model,
            on_save=self.save_new_song
        )

    def save_new_song(self, data):

        try:

            self.song_model.create(
                data["titulo"],
                data["tipo"],
                data["numero_himno"],
                data["referencia"],
                data["orden"],
                data["station_id"]
            )

        except sqlite3.IntegrityError as error:

            messagebox.showerror(
                "Error",
                f"No se pudo guardar la canción:\n\n{error}"
            )

            return False

        self.load_songs()

        return True

    # ==========================================================
    # EDITAR
    # ==========================================================

    def edit_song(self):

        song = self.get_selected_song()

        if song is None:
            return

        SongForm(
            self.window,
            self.station_model,
            song=song,
            on_save=self.save_edited_song
        )

    def save_edited_song(self, song_id, data):

        try:

            self.song_model.update(
                song_id,
                data["titulo"],
                data["tipo"],
                data["numero_himno"],
                data["referencia"],
                data["orden"],
                data["station_id"]
            )

        except sqlite3.IntegrityError as error:

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar la canción:\n\n{error}"
            )

            return False

        self.load_songs()

        return True

    # ==========================================================
    # ACTIVAR / DESACTIVAR
    # ==========================================================

    def toggle_active(self):

        song = self.get_selected_song()

        if song is None:
            return

        new_state = not bool(song["activo"])

        self.song_model.set_active(
            song["id"],
            new_state
        )

        self.load_songs()


# ==============================================================
# FORMULARIO
# ==============================================================

class SongForm:

    def __init__(
        self,
        parent,
        station_model,
        song=None,
        on_save=None
    ):

        self.station_model = station_model
        self.song = song
        self.on_save = on_save

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Nueva canción"
            if song is None
            else "Editar canción"
        )

        self.window.geometry("450x400")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_stations()

        if song is not None:
            self.load_song()

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def create_widgets(self):

        frame = ttk.Frame(
            self.window,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        # ------------------------------------------------------
        # Título
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="Título:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.titulo_var = tk.StringVar()

        ttk.Entry(
            frame,
            textvariable=self.titulo_var,
            width=40
        ).grid(
            row=0,
            column=1,
            pady=5
        )

        # ------------------------------------------------------
        # Tipo
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="Tipo:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.tipo_var = tk.StringVar(
            value="himno"
        )

        self.tipo_combo = ttk.Combobox(
            frame,
            textvariable=self.tipo_var,
            values=("himno", "alabanza"),
            state="readonly",
            width=37
        )

        self.tipo_combo.grid(
            row=1,
            column=1,
            pady=5
        )

        self.tipo_combo.bind(
            "<<ComboboxSelected>>",
            self.on_tipo_changed
        )

        # ------------------------------------------------------
        # Número de himno
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="N.º Himno:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.numero_himno_var = tk.StringVar()

        self.numero_himno_entry = ttk.Entry(
            frame,
            textvariable=self.numero_himno_var,
            width=40
        )

        self.numero_himno_entry.grid(
            row=2,
            column=1,
            pady=5
        )

        # ------------------------------------------------------
        # Referencia
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="Referencia:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.referencia_var = tk.StringVar()

        self.referencia_combo = ttk.Combobox(
            frame,
            textvariable=self.referencia_var,
            state="readonly",
            width=37
        )

        self.referencia_combo.grid(
            row=3,
            column=1,
            pady=5
        )

        # ------------------------------------------------------
        # Estación
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="Estación:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.station_var = tk.StringVar()

        self.station_combo = ttk.Combobox(
            frame,
            textvariable=self.station_var,
            state="readonly",
            width=37
        )

        self.station_combo.grid(
            row=4,
            column=1,
            pady=5
        )

        # ------------------------------------------------------
        # Orden
        # ------------------------------------------------------

        ttk.Label(
            frame,
            text="Orden:"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=5
        )

        self.orden_var = tk.StringVar()

        ttk.Entry(
            frame,
            textvariable=self.orden_var,
            width=40
        ).grid(
            row=5,
            column=1,
            pady=5
        )

        # ------------------------------------------------------
        # Botones
        # ------------------------------------------------------

        buttons = ttk.Frame(frame)

        buttons.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(25, 0)
        )

        ttk.Button(
            buttons,
            text="Guardar",
            command=self.save
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons,
            text="Cancelar",
            command=self.window.destroy
        ).pack(
            side="left",
            padx=5
        )

    # ==========================================================
    # ESTACIONES
    # ==========================================================

    def load_stations(self):

        stations = self.station_model.get_all(
            active_only=True
        )

        self.station_lookup = {}

        names = []

        for station in stations:

            name = station["nombre"]

            names.append(name)

            self.station_lookup[name] = station["id"]

        self.station_combo["values"] = names

        if names and self.song is None:
            self.station_combo.current(0)

        self.update_references()

    # ==========================================================
    # CAMBIO DE TIPO
    # ==========================================================

    def on_tipo_changed(self, event=None):

        tipo = self.tipo_var.get()

        if tipo == "himno":

            self.referencia_combo["values"] = (
                "Himnario",
            )

            self.referencia_var.set(
                "Himnario"
            )

            self.numero_himno_entry.config(
                state="normal"
            )

        else:

            self.referencia_combo["values"] = (
                "Folder",
            )

            self.referencia_var.set(
                "Folder"
            )

            self.numero_himno_var.set("")

            self.numero_himno_entry.config(
                state="disabled"
            )

    # ==========================================================
    # REFERENCIAS
    # ==========================================================

    def update_references(self):

        self.on_tipo_changed()

    # ==========================================================
    # CARGAR CANCIÓN
    # ==========================================================

    def load_song(self):

        self.titulo_var.set(
            self.song["titulo"]
        )

        self.tipo_var.set(
            self.song["tipo"]
        )

        if self.song["numero_himno"] is not None:
            self.numero_himno_var.set(
                str(self.song["numero_himno"])
            )

        self.orden_var.set(
            str(self.song["orden"])
        )

        self.station_var.set(
            self.song["station_name"]
        )

        self.on_tipo_changed()

    # ==========================================================
    # GUARDAR
    # ==========================================================

    def save(self):

        titulo = self.titulo_var.get().strip()
        tipo = self.tipo_var.get()
        numero_text = self.numero_himno_var.get().strip()
        referencia = self.referencia_var.get()
        station_name = self.station_var.get()
        orden_text = self.orden_var.get().strip()

        # -----------------------------------------
        # Validaciones
        # -----------------------------------------

        if not titulo:
            messagebox.showwarning(
                "Validación",
                "Ingrese el título de la canción."
            )
            return

        if not station_name:
            messagebox.showwarning(
                "Validación",
                "Seleccione una estación."
            )
            return

        if not orden_text:
            messagebox.showwarning(
                "Validación",
                "Ingrese el orden."
            )
            return

        try:
            orden = int(orden_text)

            if orden < 1:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Validación",
                "El orden debe ser un número entero mayor que cero."
            )
            return

        # -----------------------------------------
        # Número de himno
        # -----------------------------------------

        numero_himno = None

        if tipo == "himno":

            if not numero_text:
                messagebox.showwarning(
                    "Validación",
                    "Ingrese el número del himno."
                )
                return

            try:
                numero_himno = int(numero_text)

                if numero_himno < 1:
                    raise ValueError

            except ValueError:

                messagebox.showwarning(
                    "Validación",
                    "El número del himno debe ser un entero positivo."
                )
                return

        station_id = self.station_lookup.get(
            station_name
        )

        if station_id is None:
            messagebox.showerror(
                "Error",
                "La estación seleccionada no es válida."
            )
            return

        data = {
            "titulo": titulo,
            "tipo": tipo,
            "numero_himno": numero_himno,
            "referencia": referencia,
            "orden": orden,
            "station_id": station_id
        }

        # -----------------------------------------
        # Crear
        # -----------------------------------------

        if self.song is None:

            success = self.on_save(data)

        # -----------------------------------------
        # Editar
        # -----------------------------------------

        else:

            success = self.on_save(
                self.song["id"],
                data
            )

        if success:
            self.window.destroy()