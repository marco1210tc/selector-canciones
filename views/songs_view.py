import tkinter as tk
from tkinter import ttk, messagebox

from services.song_service import SongService


class SongsView:

    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Administrar canciones")
        self.window.geometry("900x500")
        self.window.resizable(True, True)

        self.song_service = SongService()

        self.create_widgets()
        self.load_songs()

    def create_widgets(self):
        main_frame = ttk.Frame(
            self.window,
            padding=15
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # Tabla
        # -------------------------

        columns = (
            "id",
            "titulo",
            "tipo",
            "numero_himno",
            "referencia",
            "estacion",
            "activo"
        )

        self.tree = ttk.Treeview(
            main_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading(
            "numero_himno",
            text="N.º himno"
        )
        self.tree.heading(
            "referencia",
            text="Referencia"
        )
        self.tree.heading(
            "estacion",
            text="Estación"
        )
        self.tree.heading(
            "activo",
            text="Activo"
        )

        self.tree.column("id", width=50)
        self.tree.column("titulo", width=220)
        self.tree.column("tipo", width=100)
        self.tree.column("numero_himno", width=90)
        self.tree.column("referencia", width=100)
        self.tree.column("estacion", width=160)
        self.tree.column("activo", width=70)

        scrollbar = ttk.Scrollbar(
            main_frame,
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

        # -------------------------
        # Botones
        # -------------------------

        buttons_frame = ttk.Frame(
            self.window,
            padding=(15, 0, 15, 15)
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
            command=self.toggle_song
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

    def load_songs(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        songs = self.song_service.get_all_songs()

        for song in songs:
            numero_himno = (
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
                values=(
                    song["id"],
                    song["titulo"],
                    song["tipo"],
                    numero_himno,
                    song["referencia"],
                    song["station_name"],
                    activo
                )
            )

    def get_selected_song(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Selección",
                "Debe seleccionar una canción."
            )
            return None

        item = self.tree.item(selection[0])

        song_id = item["values"][0]

        return self.song_service.get_song_by_id(song_id)

    def new_song(self):
        SongForm(
            self.window,
            self.song_service,
            on_saved=self.load_songs
        )

    def edit_song(self):
        song = self.get_selected_song()

        if song is None:
            return

        SongForm(
            self.window,
            self.song_service,
            song=song,
            on_saved=self.load_songs
        )

    def toggle_song(self):
        song = self.get_selected_song()

        if song is None:
            return

        current_active = bool(song["activo"])
        new_active = not current_active

        self.song_service.set_active(
            song["id"],
            new_active
        )

        self.load_songs()


class SongForm:

    def __init__(
        self,
        parent,
        song_service,
        song=None,
        on_saved=None
    ):
        self.parent = parent
        self.song_service = song_service
        self.song = song
        self.on_saved = on_saved

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Editar canción"
            if song
            else "Nueva canción"
        )

        self.window.geometry("450x400")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_stations()

        if self.song:
            self.load_song()

    def create_widgets(self):
        frame = ttk.Frame(
            self.window,
            padding=20
        )
        frame.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # Título
        # -------------------------

        ttk.Label(
            frame,
            text="Título:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.title_entry = ttk.Entry(
            frame,
            width=35
        )

        self.title_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=5
        )

        # -------------------------
        # Tipo
        # -------------------------

        ttk.Label(
            frame,
            text="Tipo:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.type_combo = ttk.Combobox(
            frame,
            values=("Himno", "Alabanza"),
            state="readonly",
            width=32
        )

        self.type_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=5
        )

        self.type_combo.bind(
            "<<ComboboxSelected>>",
            self.on_type_changed
        )

        # -------------------------
        # Número de himno
        # -------------------------

        ttk.Label(
            frame,
            text="N.º himno:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.hymn_number_entry = ttk.Entry(
            frame,
            width=35
        )

        self.hymn_number_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=5
        )

        # -------------------------
        # Referencia
        # -------------------------

        ttk.Label(
            frame,
            text="Referencia:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.reference_var = tk.StringVar()

        self.reference_entry = ttk.Entry(
            frame,
            textvariable=self.reference_var,
            state="readonly",
            width=35
        )

        self.reference_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=5
        )

        # -------------------------
        # Estación
        # -------------------------

        ttk.Label(
            frame,
            text="Estación:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.station_combo = ttk.Combobox(
            frame,
            state="readonly",
            width=32
        )

        self.station_combo.grid(
            row=4,
            column=1,
            sticky="ew",
            pady=5
        )

        # -------------------------
        # Botones
        # -------------------------

        buttons_frame = ttk.Frame(frame)

        buttons_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=25
        )

        ttk.Button(
            buttons_frame,
            text="Guardar",
            command=self.save
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.window.destroy
        ).pack(
            side="left",
            padx=5
        )

        frame.columnconfigure(
            1,
            weight=1
        )

    def load_stations(self):
        stations = self.song_service.get_all_stations(
            active_only=True
        )

        self.stations = stations

        self.station_combo["values"] = [
            station["nombre"]
            for station in stations
        ]

    def load_song(self):
        self.title_entry.insert(
            0,
            self.song["titulo"]
        )

        self.type_combo.set(
            self.song["tipo"]
        )

        if self.song["numero_himno"] is not None:
            self.hymn_number_entry.insert(
                0,
                self.song["numero_himno"]
            )

        for index, station in enumerate(self.stations):
            if station["id"] == self.song["station_id"]:
                self.station_combo.current(index)
                break

        self.on_type_changed()

    def on_type_changed(self, event=None):
        tipo = self.type_combo.get().lower()


        if tipo == self.song_service.song_model.tipos[0]:
            self.hymn_number_entry.config(
                state="normal"
            )

            self.reference_var.set(
                "Himnario"
            )

        elif tipo == self.song_service.song_model.tipos[1]:
            self.hymn_number_entry.delete(
                0,
                tk.END
            )

            self.hymn_number_entry.config(
                state="disabled"
            )

            self.reference_var.set(
                "Folder"
            )

        else:
            self.hymn_number_entry.config(
                state="disabled"
            )

            self.reference_var.set("")

    def save(self):
        titulo = self.title_entry.get()
        tipo = self.type_combo.get()
        numero_himno = self.hymn_number_entry.get()

        station_index = self.station_combo.current()

        if station_index == -1:
            messagebox.showwarning(
                "Datos incompletos",
                "Debe seleccionar una estación."
            )
            return

        station_id = self.stations[station_index]["id"]

        try:
            if self.song:
                self.song_service.update(
                    song_id=self.song["id"],
                    titulo=titulo,
                    tipo=tipo,
                    numero_himno=numero_himno,
                    station_id=station_id
                )
            else:
                self.song_service.create(
                    titulo=titulo,
                    tipo=tipo,
                    numero_himno=numero_himno,
                    station_id=station_id
                )

        except ValueError as error:
            messagebox.showerror(
                "Datos inválidos",
                str(error)
            )
            return

        if self.on_saved:
            self.on_saved()

        self.window.destroy()