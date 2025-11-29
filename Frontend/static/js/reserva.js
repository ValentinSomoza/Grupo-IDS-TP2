function mostrarInfoHabitacion() {
    const tipo = document.getElementById("tipo").value;
    const infoBox = document.getElementById("info-habitacion");

    const info = {
        simple:       { personas: 1, costo: 100000 },
        doble:        { personas: 2, costo: 200000 },
        matrimonial:  { personas: 2, costo: 300000 },
        ejecutivo:    { personas: 4, costo: 400000 },
        familiar:     { personas: 5, costo: 500000 },
        deluxe:       { personas: 6, costo: 600000 },
        panoramica:   { personas: 7, costo: 700000 },
        presidencial: { personas: 8, costo: 800000 }
    };

    if (info[tipo]) {
        const costoFormateado = info[tipo].costo.toLocaleString("es-AR", {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });

        infoBox.innerHTML = `
            <p><strong>Capacidad:</strong> ${info[tipo].personas} personas</p>
            <p><strong>Costo:</strong> $${costoFormateado} ARS</p>
        `;
        infoBox.style.display = "block";
    }
}