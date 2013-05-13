var popup = L.popup();

function latLngPop(e) {
    popup.setLatLng(e.latlng)
         .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                     "<br>Longitude: " + e.latlng.lng.toFixed(4))
         .openOn(map);
}

map.on('click', latLngPop);