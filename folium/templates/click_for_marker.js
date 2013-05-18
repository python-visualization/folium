function newMarker(e){
    var new_mark = L.marker().setLatLng(e.latlng).addTo(map);
    new_mark.dragging.enable();
    new_mark.on('dblclick', function(e){map.removeLayer(e.target)})
    var lat = e.latlng.lat.toFixed(4),
       lng = e.latlng.lng.toFixed(4);
    new_mark.bindPopup({{ popup }});
};
map.on('click', newMarker)