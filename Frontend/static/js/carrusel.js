new Swiper(".swiper", {
    slidesPerView: "auto",
    centeredSlides: false,
    spaceBetween: 8,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});