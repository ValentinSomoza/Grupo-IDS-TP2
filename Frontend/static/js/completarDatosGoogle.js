document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector("header, nav, .navbar, .menu");
    const footer = document.querySelector("footer");

    if (navbar) {
        navbar.style.pointerEvents = "none";
        navbar.style.opacity = "0.5";
    }

    if (footer) {
        footer.style.pointerEvents = "none";
        footer.style.opacity = "0.5";
    }
});