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

from branca.element import MacroElement, Figure, JavascriptLink, CssLink
from branca.utilities import none_min, none_max, iter_points


class TimestampedGeoJson(MacroElement):
    def __init__(self, data, transition_time=200, loop=True, auto_play=True,
                 period="P1D"):
        """Creates a TimestampedGeoJson plugin to append into a map with
        Map.add_child.

        Parameters
        ----------
        data: file, dict or str.
           The timestamped geo-json data you want to plot.

           * If file, then data will be read in the file and fully
             embedded in Leaflet's javascript.
           * If dict, then data will be converted to json and embedded in
             the javascript.
           * If str, then data will be passed to the javascript as-is.

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
            The duration in ms of a transition from between timestamps.
        loop : bool, default True
            Whether the animation shall loop.
        auto_play : bool, default True
            Whether the animation shall start automatically at startup.
        period : str, default "P1D"
            Used to construct the array of available times starting
            from the first available time. Format: ISO8601 Duration
            ex: "P1M" -> 1/month
                "P1D"  -> 1/day
                "PT1H"  -> 1/hour
                "PT1M"  -> 1/minute
        """
        super(TimestampedGeoJson, self).__init__()
        self._name = 'TimestampedGeoJson'

        # self.template = self.env.get_template('timestamped_geo_json.tpl')
        if 'read' in dir(data):
            self.embed = True
            self.data = data.read()
        elif type(data) is dict:
            self.embed = True
            self.data = json.dumps(data)
        else:
            self.embed = False
            self.data = data
        self.transition_time = int(transition_time)
        self.loop = bool(loop)
        self.auto_play = bool(auto_play)
        self.period = period

        self._template = Template("""
        {% macro script(this, kwargs) %}
            {{this._parent.get_name()}}.timeDimension = L.timeDimension({period:"{{this.period}}"});
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
        """)  # noqa

    def render(self, **kwargs):
        super(TimestampedGeoJson, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js"),  # noqa
            name='jquery2.0.0')

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"),  # noqa
            name='jqueryui1.10.2')

        figure.header.add_child(
            JavascriptLink("https://rawgit.com/nezasa/iso8601-js-period/master/iso8601.min.js"),  # noqa
            name='iso8601')

        figure.header.add_child(
            JavascriptLink("https://rawgit.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"),  # noqa
            name='leaflet.timedimension')

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css"),  # noqa
            name='highlight.js_css')

        figure.header.add_child(
            CssLink("http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css"),  # noqa
            name='leaflet.timedimension_css')

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        if not self.embed:
            raise ValueError('Cannot compute bounds of non-embedded GeoJSON.')

        data = json.loads(self.data)
        if 'features' not in data.keys():
            # Catch case when GeoJSON is just a single Feature or a geometry.
            if not (isinstance(data, dict) and 'geometry' in data.keys()):
                # Catch case when GeoJSON is just a geometry.
                data = {'type': 'Feature', 'geometry': data}
            data = {'type': 'FeatureCollection', 'features': [data]}

        bounds = [[None, None], [None, None]]
        for feature in data['features']:
            for point in iter_points(feature.get('geometry', {}).get('coordinates', {})):  # noqa
                bounds = [
                    [
                        none_min(bounds[0][0], point[1]),
                        none_min(bounds[0][1], point[0]),
                        ],
                    [
                        none_max(bounds[1][0], point[1]),
                        none_max(bounds[1][1], point[0]),
                        ],
                    ]
        return bounds
