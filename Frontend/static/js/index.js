async function cargarImagenesIndex() {
    try {
        const respuesta = await fetch(`${BACKEND_URL}/datosIndex/imagenesIndex`);
        const imagenesPorTipo = await respuesta.json();

        function construirRuta(rutaBD) {
            rutaBD = rutaBD.replace(/^\/+/, '');
            return `${window.location.origin}/${rutaBD}`;
        }

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

cargarImagenesIndex();