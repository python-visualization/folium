var {{ circle }} = L.circleMarker([{{ lat }}, {{ lon }}], {
                            color: '{{ line_color }}',
                            fillColor: '{{ fill_color }}',
                            weight: {{ weight }},
                            fillOpacity: {{ fill_opacity }}
                            }).setRadius({{ radius }})
