# -*- coding: utf-8 -*-
'''
Folium Plugins Tests
--------------------

'''
import folium
from folium import plugins
import numpy as np
import json

class testPlugins(object):
    '''Test class for Folium plugins'''

    def test_scroll_zoom_toggler(self):
        mapa = folium.Map([45.,3.], zoom_start=4)
        mapa.add_plugin(plugins.ScrollZoomToggler())
        mapa._build_map()

        
    def test_marker_cluster(self):
        N = 100
        data = np.array([
            np.random.uniform(low=35,high=60, size=N),   # random latitudes in Europe
            np.random.uniform(low=-12,high=30, size=N),  # random longitudes in Europe
            range(N),                                    # popups are simple numbers 
            ]).T
        mapa = folium.Map([45.,3.], zoom_start=4)
        mapa.add_plugin(plugins.MarkerCluster(data))
        mapa._build_map()

    def test_terminator(self):
        mapa = folium.Map([45.,3.], zoom_start=1)
        mapa.add_plugin(plugins.Terminator())
        mapa.add_plugin(plugins.ScrollZoomToggler())
        mapa._build_map()

    def test_boat_marker(self):
        mapa = folium.Map([30.,0.], zoom_start=3)
        mapa.add_plugin(plugins.BoatMarker((34,-43), heading=45,
                                            wind_heading=150, wind_speed=45, color="#8f8"))
        mapa.add_plugin(plugins.BoatMarker((46,-30), heading=-20,
                                            wind_heading=46, wind_speed=25, color="#88f"))
        mapa._build_map()

    def test_layer(self):
        mapa = folium.Map([48.,5.], zoom_start=6)
        mapa.add_plugin(plugins.Layer('//otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
                                      layer_name='MapQuest'))
        mapa.add_plugin(plugins.LayerControl())
        mapa._build_map()

    def test_geo_json(self):
        N=100
        lons = +5 - np.random.normal(size=N)
        lats = 48 - np.random.normal(size=N)

        data = {
            "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiPoint",
                            "coordinates": [[lon, lat] for (lat,lon) in zip(lats,lons)],
                            },
                        "properties": {"prop0": "value0"}
                        },
                ],
            }

        mapa = folium.Map([48.,5.], zoom_start=6)
        mapa.add_plugin(plugins.GeoJson(data))
        mapa._build_map()

        open('geojson_plugin_test1.json','w').write(json.dumps(data))
        mapb = folium.Map([48.,5.], zoom_start=6)
        mapb.add_plugin(plugins.GeoJson(open('geojson_plugin_test1.json')))
        mapb._build_map()

        data = {
            "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": [[[[lon+1e-4, lat+1e-4],
                                             [lon+1e-4, lat-1e-4],
                                             [lon-1e-4, lat-1e-4],
                                             [lon-1e-4, lat+1e-4]]] for (lat,lon) in zip(lats,lons)],
                            },
                        "properties": {"prop0": "value0"}
                        },
                ],
            }

        mapc = folium.Map([48.,5.], zoom_start=6)
        mapc.add_plugin(plugins.GeoJson(data))
        mapc._build_map()

        open('geojson_plugin_test2.json','w').write(json.dumps(data))
        mapd = folium.Map([48.,5.], zoom_start=6)
        mapd.add_plugin(plugins.GeoJson(open('geojson_plugin_test2.json')))
        mapd._build_map()

