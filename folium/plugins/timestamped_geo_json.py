# -*- coding: utf-8 -*-
"""
TimestampedGeoJson plugin
--------------

Add a timestamped geojson feature collection on a folium map.
This is based on Leaflet.TimeDimension.

https://github.com/socib/Leaflet.TimeDimension

A geo-json is timestamped if:
    * it contains only features of types LineString, MultiPoint,
      MultiLineString and MultiPolygon.
    * each feature has a "times" property with the same length as the
      coordinates array.
    * each element of each "times" property is a timestamp in ms since epoch,
     or in ISO string.  Eventually, you may have Point features with a
     "times" property being an array of length 1.

"""

import json
from jinja2 import Template

from folium.element import MacroElement, Figure, JavascriptLink, CssLink


class TimestampedGeoJson(MacroElement):
    def __init__(self, data, transition_time=200, loop=True, auto_play=True):
        """Creates a TimestampedGeoJson plugin to append into a map with
        Map.add_children.

        Parameters
        ----------
            data: file, dict or str.
                The timestamped geo-json data you want to plot.

                If file, then data will be read in the file and fully embedded in Leaflet's javascript.
                If dict, then data will be converted to json and embeded in the javascript.
                If str, then data will be passed to the javascript as-is.

                A geo-json is timestamped if:
                    * it contains only features of types LineString,
                      MultiPoint, MultiLineString and MultiPolygon.
                    * each feature has a "times" property with the same length
                      as the coordinates array.
                    * each element of each "times" property is a timestamp in
                      ms since epoch, or in ISO string.
                    Eventually, you may have Point features with a "times"
                    property being an array of length 1.

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
        self._name = 'TimestampedGeoJson'

        # self.template = self.env.get_template('timestamped_geo_json.tpl')
        if 'read' in dir(data):
            self.data = data.read()
        elif type(data) is dict:
            self.data = json.dumps(data)
        else:
            self.data = data
        self.transition_time = int(transition_time)
        self.loop = bool(loop)
        self.auto_play = bool(auto_play)

        self._template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.timeDimension = L.timeDimension();
            {{this._parent.get_name()}}.timeDimensionControl = L.control.timeDimension({
                position: 'bottomleft',
                autoPlay: {{'true' if this.auto_play else 'false'}},
                playerOptions: {
                    transitionTime: {{this.transition_time}},
                    loop: {{'true' if this.loop else 'false'}}}
                    });
            {{this._parent.get_name()}}.addControl({{this._parent.get_name()}}.timeDimensionControl);

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(
                L.geoJson({{this.data}}),
                {updateTimeDimension: true,addlastPoint: true}
                ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def render(self, **kwargs):
        super(TimestampedGeoJson, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js"),
            name='jquery2.0.0')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"),
            name='jqueryui1.10.2')

        figure.header.add_children(
            JavascriptLink("https://raw.githubusercontent.com/nezasa/iso8601-js-period/master/iso8601.min.js"),
            name='iso8601')

        figure.header.add_children(
            JavascriptLink("https://raw.githubusercontent.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"),
            name='leaflet.timedimension')

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css"),
            name='highlight.js_css')

        figure.header.add_children(
            CssLink("http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"),
            name='leaflet.timedimension_css')
