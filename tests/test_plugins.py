# -*- coding: utf-8 -*-

"""
Folium Plugins Tests
--------------------

"""

import folium
from folium import plugins
import numpy as np
import json


class TestPlugins(object):
    """Test class for Folium plugins."""

    def test_scroll_zoom_toggler(self):
        mapa = folium.Map([45., 3.], zoom_start=4)
        mapa.add_children(plugins.ScrollZoomToggler())
        mapa._repr_html_()

    def test_marker_cluster(self):
        N = 100
        data = np.array([
            np.random.uniform(low=35, high=60, size=N),   # Random latitudes.
            np.random.uniform(low=-12, high=30, size=N),  # Random longitudes.
            range(N),                                    # Popups.
            ]).T
        mapa = folium.Map([45., 3.], zoom_start=4)
        mapa.add_children(plugins.MarkerCluster(data))
        mapa._repr_html_()

    def test_terminator(self):
        mapa = folium.Map([45., 3.], zoom_start=1)
        mapa.add_children(plugins.Terminator())
        mapa.add_children(plugins.ScrollZoomToggler())
        mapa._repr_html_()

    def test_boat_marker(self):
        mapa = folium.Map([30., 0.], zoom_start=3)
        mapa.add_children(plugins.BoatMarker((34, -43),
                                           heading=45,
                                           wind_heading=150,
                                           wind_speed=45,
                                           color="#8f8"))
        mapa.add_children(plugins.BoatMarker((46, -30),
                                           heading=-20,
                                           wind_heading=46,
                                           wind_speed=25,
                                           color="#88f"))
        mapa._repr_html_()

    def test_layer(self):
        mapa = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
        layer = 'http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png'
        mapa.add_children(folium.map.TileLayer(layer, name='MapQuest',  attr='attribution'))
        mapa.add_children(folium.map.TileLayer(layer, name='MapQuest2', attr='attribution2', overlay=True))
        mapa.add_children(folium.map.LayerControl())
        mapa._repr_html_()

    def test_timestamped_geo_json(self):
        coordinates = [[[[lon-8*np.sin(theta), -47+6*np.cos(theta)] for
                         theta in np.linspace(0, 2*np.pi, 25)],
                        [[lon-4*np.sin(theta), -47+3*np.cos(theta)] for theta
                         in np.linspace(0, 2*np.pi, 25)]] for
                       lon in np.linspace(-150, 150, 7)]
        data = {
            "type": "FeatureCollection",
            "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [0, 0],
                            },
                        "properties": {
                            "times": [1435708800000+12*86400000]
                            }
                        },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiPoint",
                            "coordinates": [[lon, -25] for
                                            lon in np.linspace(-150, 150, 49)],
                            },
                        "properties": {
                            "times": [1435708800000+i*86400000 for
                                      i in np.linspace(0, 25, 49)]
                            }
                        },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[lon, 25] for
                                            lon in np.linspace(-150, 150, 25)],
                            },
                        "properties": {
                            "times": [1435708800000+i*86400000 for
                                      i in np.linspace(0, 25, 25)]
                            }
                        },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiLineString",
                            "coordinates": [[[lon-4*np.sin(theta),
                                              47+3*np.cos(theta)] for theta
                                             in np.linspace(0, 2*np.pi, 25)]
                                            for lon in
                                            np.linspace(-150, 150, 13)],
                            },
                        "properties": {
                            "times": [1435708800000+i*86400000 for
                                      i in np.linspace(0, 25, 13)]
                            }
                        },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": coordinates,
                            },
                        "properties": {
                            "times": [1435708800000+i*86400000 for
                                      i in np.linspace(0, 25, 7)]
                            }
                        },
                ],
            }

        mape = folium.Map([47, 3], zoom_start=1)
        mape.add_children(plugins.TimestampedGeoJson(data))
        mape._repr_html_()

    def test_heat_map(self):
        data = (np.random.normal(size=(100,2))*np.array([[1,1]])+np.array([[48,5]])).tolist()
        mapa = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
        mapa.add_children(plugins.HeatMap(data))
        mapa._repr_html_()
