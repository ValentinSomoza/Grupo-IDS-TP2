async function cargarImagenes() {
    const respuesta = await fetch(`${BACKEND_URL}/datosIndex/imagenesHotel`);
    const imagenes = await respuesta.json(); 

    const contenedor = document.getElementById("galeria-swiper-wrapper");
    contenedor.innerHTML = "";

    imagenes.forEach((url, index) => {
        const slide = document.createElement("div");
        slide.classList.add("swiper-slide");

        slide.innerHTML = `
            <img 
                src="/${url}"
                class="miniatura"
                alt="Imagen ${index + 1}"
                loading="lazy"
                data-index="${index}">
        `;

        contenedor.appendChild(slide);
    });

    inicializarCarrusel();
    inicializarModal();
}

function inicializarCarrusel() {

    const swiper = new Swiper(".swiper", {
        slidesPerView: 1.2,
        centeredSlides: true,
        spaceBetween: 10,
        loop: true,

        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
    });

    const swiperContainer = document.querySelector(".swiper");

    swiperContainer.addEventListener("wheel", (e) => {
        e.preventDefault();

        if (e.deltaY > 0) {
            swiper.slideNext();
        } else {
            swiper.slidePrev();
        }
    });
}

function inicializarModal() {
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
}

cargarImagenes();