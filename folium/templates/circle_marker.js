var {{ circle }} = L.circleMarker([{{ lat }}, {{ lon }}], {
                            color: '{{ line_color }}',
                            weight: {{ weight }},
                            fillColor: '{{ fill_color }}',
                            fillOpacity: {{ fill_opacity }}
                            }).setRadius({{ radius }})
