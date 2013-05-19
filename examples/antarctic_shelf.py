'''
Map the Antarctic Ice Shelf, with normal GeoJSON and TopoJSON

'''

import folium


path = r'data/antarctic_ice_edge.json'
path1 = r'data/antarctic_ice_shelf_topo.json'

map_1 = folium.Map(location=[-59.1759, -11.6016],
                   tiles='Mapbox Bright', zoom_start=2)
map_1.geo_json(geo_path=path)
map_1.geo_json(geo_path=path1, topojson='objects.antarctic_ice_shelf')
map_1.create_map()
