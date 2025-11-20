function mostrarInfoHabitacion() {
    const tipo = document.getElementById("tipo").value;
    const infoBox = document.getElementById("info-habitacion");

    const info = {
        simple:     { personas: 1, costo: 10 },
        doble:      { personas: 2, costo: 20 },
        matrimonial:{ personas: 2, costo: 30 },
        king:       { personas: 3, costo: 50 },
        suite:      { personas: 4, costo: 40 },
    };

    if (info[tipo]) {
        infoBox.innerHTML = `
            <p><strong>Capacidad:</strong> ${info[tipo].personas} personas</p>
            <p><strong>Costo:</strong> $${info[tipo].costo} ARS</p>
        `;
        infoBox.style.display = "block";
    }
}