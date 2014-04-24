var {{ marker }} = new L.RegularPolygonMarker(new L.LatLng({{ lat}}, {{ lon }}), {
    color: '{{ line_color }}',
    opacity: {{ line_opacity }},
    weight: {{ line_weight }},
    fillColor: '{{ fill_color }}',
    fillOpacity: {{ fill_opacity }},
    numberOfSides: {{ num_sides }},
    rotation: {{ rotation }},
    radius: {{ radius }}
});
