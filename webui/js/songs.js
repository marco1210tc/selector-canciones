
const Songs = {

    async getAll() {
        const response = await window.pywebview.api.initial_data();

        if (!response.ok) {
            throw new Error(response.error);
        }

        return response.data.songs;
    },

    async render() {
        const tbody = document.getElementById("songsTable");

        if (!tbody) {
            console.error("No existe el elemento #songsTable");
            return;
        }

        try {
            const songs = await this.getAll();

            console.log("Canciones recibidas:", songs);

            tbody.replaceChildren();

            songs.forEach(song => {
                const tr = document.createElement("tr");

                const values = [
                    song.id,
                    song.titulo,
                    song.tipo,
                    song.numero_himno ?? "-",
                    song.referencia,
                    song.station_name,
                    song.activo ? "Activo" : "Inactivo"
                ];

                values.forEach(value => {
                    const td = document.createElement("td");
                    td.textContent = value ?? "";
                    td.className = "px-4 py-3 text-sm";
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });

        } catch (error) {
            console.error("Error al cargar canciones:", error);
            alert("Error al cargar canciones: " + error);
        }
    }

};

window.addEventListener("pywebviewready", () => {
    Songs.render();
});
