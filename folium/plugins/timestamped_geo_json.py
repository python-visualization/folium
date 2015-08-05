# -*- coding: utf-8 -*-
"""
TimestampedGeoJson plugin
--------------

Add a timestamped geojson feature collection on a folium map.
This is based on Leaflet.TimeDimension (see https://github.com/socib/Leaflet.TimeDimension).

A geo-json is timestamped if :
    * it contains only features of types LineString, MultiPoint, MultiLineString and MultiPolygon.
    * each feature has a "times" property with the same length as the coordinates array.
    * each element of each "times" property is a timestamp in ms since epoch, or in ISO string.
    Eventually, you may have Point features with a "times" property being an array of length 1.
"""
import json

from .plugin import Plugin

class TimestampedGeoJson(Plugin):
    """Adds a TimestampedGeoJson layer on the map."""
    def __init__(self, data, transition_time=200, loop=True, auto_play=True):
        """Creates a TimestampedGeoJson plugin to append into a map with
        Map.add_plugin.

        Parameters
        ----------
            data: file, dict or str.
                The timestamped geo-json data you want to plot.

                If file, then data will be read in the file and fully embeded in Leaflet's javascript.
                If dict, then data will be converted to json and embeded in the javascript.
                If str, then data will be passed to the javascript as-is.

                A geo-json is timestamped if :
                    * it contains only features of types LineString, MultiPoint, MultiLineString and MultiPolygon.
                    * each feature has a "times" property with the same length as the coordinates array.
                    * each element of each "times" property is a timestamp in ms since epoch, or in ISO string.
                    Eventually, you may have Point features with a "times" property being an array of length 1.

                examples :
                    # providing file
                    TimestampedGeoJson(open('foo.json'))

                    # providing dict
                    TimestampedGeoJson({
                        "type": "FeatureCollection",
                            "features": [
                                {
                                    "type": "Feature",
                                    "geometry": {
                                        "type": "LineString",
                                        "coordinates": [[-70,-25],[-70,35],[70,35]],
                                        },
                                    "properties": {
                                        "times": [1435708800000, 1435795200000, 1435881600000]
                                        }
                                    }
                                ]
                            })

                    # providing string
                    TimestampedGeoJson(open('foo.json').read())
            transition_time : int, default 200.
                The duration in ms of a transition from one timestamp to another.
            loop : bool, default True
                Whether the animation shall loop.
            auto_play : bool, default True
                Whether the animation shall start automatically at startup.
            
        """
        super(TimestampedGeoJson, self).__init__()
        self.plugin_name = 'TimestampedGeoJson'
        self.template = self.env.get_template('timestamped_geo_json.tpl')
        if 'read' in dir(data):
            self.data = data.read()
        elif type(data) is dict:
            self.data = json.dumps(data)
        else:
            self.data = data
        self.transition_time = int(transition_time)
        self.loop = bool(loop)
        self.auto_play = bool(auto_play)

    def render_header(self, nb):
        """Generates the header part of the plugin."""
        header = self.template.module.__dict__.get('header',None)
        assert header is not None, "This template must have a 'header' macro."
        return header(nb)
    def render_js(self, nb):
        """Generates the Javascript part of the plugin."""
        js = self.template.module.__dict__.get('js',None)
        assert js is not None, "This template must have a 'js' macro."
        return js(nb,self)
