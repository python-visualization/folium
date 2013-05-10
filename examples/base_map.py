# -*- coding: utf-8 -*-
'''Test of Folium basic map'''

import folium

#Standard OSM
map_osm = folium.Map(location=[45.5236, -122.6750])
map_osm.create_map(path='osm.html')

# -*- coding: utf-8 -*-
'''Test of Folium MapBox Control Room'''

import folium

#Standard MapBox Control Room (Dark)
mapbox = folium.Map(location=[45.5236, -122.6750], tiles='MapBox Dark',
                 zoom_start=4, max_zoom=8)
mapbox.create_map(path='mapbox_dark.html')
