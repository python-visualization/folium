# -*- coding: utf-8 -*-
'''Test of Folium basic map'''

import folium

# Standard OSM.
map_osm = folium.Map(location=[45.5236, -122.6750])
map_osm.save(outfile='osm.html')

# Stamen Toner.
stamen = folium.Map(location=[45.5236, -122.6750], tiles='Stamen Toner',
                    zoom_start=13)
stamen.save(outfile='stamen_toner.html')
