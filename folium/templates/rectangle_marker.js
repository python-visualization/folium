var {{ RectangleMarker }} = L.rectangle([[{{location[0]}}, {{location[1]}}],
                                [{{location[2]}}, {{location[3]}}]],
                               {
                                   color:'{{ color }}',
                                   fillColor:'{{ fill_color }}',
                                   fillOpacity:{{ fill_opacity }},
                                   weight:{{ weight }}
                               });
