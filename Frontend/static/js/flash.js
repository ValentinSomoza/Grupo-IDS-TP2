setTimeout(() => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        flash.classList.add('hide');
    });

    setTimeout(() => {
        flashes.forEach(flash => flash.remove());
    }, 1000); 
}, 3000);