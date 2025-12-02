async function cargarImagenesIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/imagenesIndex`);
        const imagenesPorTipo = await respuesta.json();

        function construirRuta(rutaBD) {
            if (!rutaBD.startsWith("/")) {
                rutaBD = "/" + rutaBD;
            }
            return rutaBD;
        }

        // function construirRuta(rutaBD) {
        //     rutaBD = rutaBD.replace(/^\/+/, '');
        //     return `${window.location.origin}/${rutaBD}`;
        // }

        const heroWrapper = document.querySelector(".hero-swiper .swiper-wrapper");
        const showcase = imagenesPorTipo.showcase || [];

        if (heroWrapper && showcase.length > 0) {

            heroWrapper.innerHTML = "";

            showcase.forEach(ruta => {
                const slide = document.createElement("div");
                slide.classList.add("swiper-slide");

                slide.innerHTML = `
                    <div class="slide-content">
                        <img src="${construirRuta(ruta)}" alt="Hotel">
                    </div>
                `;

                heroWrapper.appendChild(slide);
            });

            if (window.heroSwiper) {
                try { window.heroSwiper.destroy(true, true); } catch (e) {}
            }

            window.heroSwiper = new Swiper(".hero-swiper", {
                loop: true,
                slidesPerView: 1,
                centeredSlides: true,
                spaceBetween: 0,
                autoplay: { delay: 5000, disableOnInteraction: false },
                navigation: {
                    nextEl: ".hero-button-next",
                    prevEl: ".hero-button-prev",
                },
                pagination: {
                    el: ".hero-pagination",
                    clickable: true,
                },
                observer: true,
                observeParents: true,
                watchOverflow: true,

                on: {
                    slideChangeTransitionEnd: function () {
                        this.update();
                        try {
                            this.slideToLoop(this.realIndex, 0, false);
                        } catch (e) {}
                    },
                    resize: function () {
                        this.update();
                    }
                }
            });

            const images = heroWrapper.querySelectorAll("img");
            let loadedCount = 0;

            images.forEach(img => {
                if (img.complete) loadedCount++;
                else img.onload = () => {
                    loadedCount++;
                    if (loadedCount === images.length) window.heroSwiper.update();
                };
            });

            if (loadedCount === images.length) window.heroSwiper.update();
        }

        const habitaciones = imagenesPorTipo.habitaciones || [];

        if (habitaciones.length > 0) {
            habitaciones.forEach((ruta, index) => {
                const habitacionImg = document.getElementById(`habitacion-${index + 1}`);
                if (habitacionImg) habitacionImg.src = construirRuta(ruta);
            });
        }

        const amenities = imagenesPorTipo.amenities || [];

        if (amenities.length > 0) {
            amenities.forEach((ruta, index) => {
                const amenityImg = document.getElementById(`amenity-${index + 1}`);
                if (amenityImg) amenityImg.src = construirRuta(ruta);
            });
        }

        const personas = imagenesPorTipo.personas || [];

        if (personas.length > 0) {
            personas.forEach((ruta, index) => {
                const personaImg = document.getElementById(`person-${index + 1}`);
                if (personaImg) personaImg.src = construirRuta(ruta);
            });
        }

        console.log("[INFO] Imágenes del index cargadas correctamente.");

    } catch (error) {
        console.error("Error cargando imágenes del index:", error);
    }
}

async function cargarTextosIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/textos`);
        const textos = await respuesta.json();

        const { habitacion = [], servicio = [], resenia = [] } = textos;

        habitacion.forEach((item, index) => {
            const numero = index + 1;

            const titulo = document.querySelector(`#amenities-cards h2`);
            const cardTitulo = document.querySelector(`#habitacion-${numero}`)?.closest(".facility-card")?.querySelector("h4");
            const precio = document.querySelector(`#habitacion-${numero}`)?.closest(".facility-card")?.querySelector(".price-tag");

            if (cardTitulo) cardTitulo.textContent = item.nombre;
            if (precio) precio.insertAdjacentHTML("afterend", `<p>${item.descripcion}</p>`);
        });

        servicio.forEach((item, index) => {
            const numero = index + 1;

            const card = document.getElementById(`amenity-${numero}`)?.closest(".facility-card");
            if (!card) return;

            const titulo = card.querySelector("h4");
            const descripcion = card.querySelector("p");

            if (titulo) titulo.textContent = item.nombre;
            if (descripcion) descripcion.textContent = item.descripcion;
        });

        resenia.forEach((item, index) => {
            const numero = index + 1;

            const testimonialCard = document.querySelector(`#person-${numero}`)?.closest(".testimonial-card");
            if (!testimonialCard) return;

            const contenido = testimonialCard.querySelector(".testimonial-content p");
            const autor = testimonialCard.querySelector(".author-info h4");

            if (contenido) contenido.textContent = `"${item.descripcion}"`;
            if (autor) autor.textContent = item.nombre;
        });

        console.log("[INFO] Textos del index cargados correctamente.");

    } catch (error) {
        console.error("Error cargando textos del index:", error);
    }
}

async function cargarHabitacionesIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/habitaciones`);
        const habitaciones = await respuesta.json();

        habitaciones.forEach((hab, index) => {
            const card = document.getElementById(`habitacion-${index + 1}`)?.closest(".facility-card");
            if (!card) return;

            const titulo = card.querySelector("h4");
            const precio = card.querySelector(".price-tag");

            const precioFormateado = new Intl.NumberFormat('es-AR', {
                style: 'currency',
                currency: 'ARS',
                minimumFractionDigits: 0
            }).format(hab.precio);

            if (titulo) {
                titulo.textContent = `Habitación ${hab.tipo.charAt(0).toUpperCase() + hab.tipo.slice(1)}`;
            }

            if (precio) {
                precio.innerHTML = `${precioFormateado}<span>/noche</span>`;
            }
        });

        console.log("[INFO] Habitaciones del index cargadas correctamente.");
    } catch (error) {
        console.error("Error cargando información de habitaciones:", error);
    }
}

function formatearPrecio(precio) {
    return new Intl.NumberFormat("es-AR", {
        style: "currency",
        currency: "ARS",
        minimumFractionDigits: 0,
    }).format(precio);
}

async function cargarHeroIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/textos`);
        const textos = await respuesta.json();

        const heroTitulo = document.querySelector(".hero-content h1");
        const heroDescripcion = document.querySelector(".hero-content .lead");

        const indexTextos = textos.index || []; // <--- ahora sí accedemos al tipo "index"
        let titulo = "";
        let descripcion = "";

        indexTextos.forEach(t => {
            if (t.nombre === "titulo_index") titulo = t.descripcion;
            if (t.nombre === "descripcion_index") descripcion = t.descripcion;
        });

        if (heroTitulo && titulo) heroTitulo.textContent = titulo;
        if (heroDescripcion && descripcion) heroDescripcion.textContent = descripcion;

        console.log("[INFO] Hero del index cargado correctamente.");

    } catch (error) {
        console.error("Error cargando hero del index:", error);
    }
}

async function cargarStatsIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/stats`);
        const stats = await respuesta.json();

        document.getElementById("num-habitaciones").textContent = stats.habitaciones;
        document.getElementById("num-personas").textContent = stats.personas_satisfechas;

    } catch (error) {
        console.error("Error cargando estadísticas del index:", error);
    }
}

async function cargarHabitacionesDisponiblesHoy() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/habitaciones-disponibles`);
        const data = await respuesta.json();

        const spanHabitacionesDisponibles = document.querySelector("#num-habitaciones-disponibles");
        if (spanHabitacionesDisponibles) {
            spanHabitacionesDisponibles.textContent = data.habitacionesDisponibles;
        }

    } catch (error) {
        console.error("Error cargando habitaciones disponibles:", error);
    }
}

cargarImagenesIndex();
cargarTextosIndex();
cargarHabitacionesIndex();
cargarHeroIndex();
cargarStatsIndex();
cargarHabitacionesDisponiblesHoy();