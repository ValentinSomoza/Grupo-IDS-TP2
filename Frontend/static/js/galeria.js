const miniaturas = document.querySelectorAll('.miniatura');
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const btnCerrar = document.getElementById('cerrar');
const flechaIzq = document.getElementById('flecha-izq');
const flechaDer = document.getElementById('flecha-der');

let indiceActual = 0;

miniaturas.forEach(img => {
    img.addEventListener('click', () => {
        indiceActual = parseInt(img.dataset.index);
        modalImg.src = img.src;
        modal.style.display = 'flex';
    });
});

function siguiente() {
    indiceActual = (indiceActual + 1) % miniaturas.length;
    modalImg.src = miniaturas[indiceActual].src;
}

function anterior() {
    indiceActual = (indiceActual - 1 + miniaturas.length) % miniaturas.length;
    modalImg.src = miniaturas[indiceActual].src;
}

flechaDer.addEventListener('click', siguiente);
flechaIzq.addEventListener('click', anterior);

btnCerrar.addEventListener('click', () => {
    modal.style.display = 'none';
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = "none";
});

document.addEventListener('keydown', (e) => {
    if (modal.style.display === 'flex') {
        if (e.key === "ArrowRight") siguiente();
        if (e.key === "ArrowLeft") anterior();
        if (e.key === "Escape") modal.style.display = "none";
    }
});