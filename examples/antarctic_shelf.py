'''
Map the Antarctic Ice Shelf, with normal GeoJSON and TopoJSON

'''

import folium


geo_path = r'data/antarctic_ice_edge.json'
topo_path = r'data/antarctic_ice_shelf_topo.json'

ice_map = folium.Map(location=[-59.1759, -11.6016],
                     tiles='Mapbox Bright', zoom_start=2)
ice_map.geo_json(geo_path=geo_path)
ice_map.geo_json(geo_path=topo_path, topojson='objects.antarctic_ice_shelf')
ice_map.create_map()
