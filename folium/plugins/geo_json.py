# -*- coding: utf-8 -*-
"""
GeoJson plugin
--------------

Add a geojson feature collection on a folium map.
"""
import json

from .plugin import Plugin

class GeoJson(Plugin):
    """Adds a GeoJson layer on the map."""
    def __init__(self, data):
        """Creates a GeoJson plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            data: file, dict or str.
                The geo-json data you want to plot.
                If file, then data will be read in the file and fully embeded in Leaflet's javascript.
                If dict, then data will be converted to json and embeded in the javascript.
                If str, then data will be passed to the javascript as-is.

                examples :
                    # providing file
                    GeoJson(open('foo.json'))

                    # providing dict
                    GeoJson(json.load(open('foo.json')))

                    # providing string
                    GeoJson(open('foo.json').read())
        """
        super(GeoJson, self).__init__()
        self.plugin_name = 'GeoJson'
        if 'read' in dir(data):
            self.data = data.read()
        elif type(data) is dict:
            self.data = json.dumps(data)
        else:
            self.data = data

    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        out = """
        var geojson_{nb} = L.geoJson({data}).addTo(map);
        """.format(nb=nb, data = self.data)
        return out
