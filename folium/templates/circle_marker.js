var {{ circle }} = L.circleMarker([{{ lat }}, {{ lon }}], {
                            color: '{{ line_color }}',
                            fillColor: '{{ fill_color }}',
                            fillOpacity: {{ fill_opacity }}
                            }).setRadius({{ radius }})