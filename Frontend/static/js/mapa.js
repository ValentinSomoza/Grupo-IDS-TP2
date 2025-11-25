var HotelIcon = L.icon({
    iconUrl: "/static/img/favicon.png",
    iconSize:     [38, 40],
    iconAnchor:   [20, 84],
    popupAnchor:  [-3, -76]
});

const coordHotel = [-34.617, -58.362]

let map = L.map('map').setView(coordHotel, 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

let marker = L.marker(coordHotel, {icon: HotelIcon}).addTo(map);
marker.bindPopup("<b>Estancia Bruno<br>Relax and Flask</b>").openPopup();

map.locate({setView: true, maxZoom: 10});

map.on('locationfound', function(e) {
    L.marker(e.latlng).addTo(map)
        .bindPopup("Estás aquí").openPopup();
});

navigator.geolocation.getCurrentPosition(function(pos) {
    let origen = L.latLng(pos.coords.latitude, pos.coords.longitude);
    let destino = L.latLng(coordHotel);

    L.Routing.control({
        waypoints: [origen, destino],
        router: L.Routing.osrmv1({
            serviceUrl: 'https://router.project-osrm.org/route/v1'
        }),
    routeWhileDragging: true,
    showAlternatives: false
    }).addTo(map).on('routesfound', function(e) {
        document.querySelector('.leaflet-routing-container').style.display = 'none';
        });
});
