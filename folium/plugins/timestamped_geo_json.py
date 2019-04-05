# -*- coding: utf-8 -*-

import json

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from folium.folium import Map
from folium.utilities import iter_points, none_max, none_min, parse_options

from jinja2 import Template


class TimestampedGeoJson(MacroElement):
    """
    Creates a TimestampedGeoJson plugin from timestamped GeoJSONs to append
    into a map with Map.add_child.

    A geo-json is timestamped if:

    * it contains only features of types LineString, MultiPoint, MultiLineString,
      Polygon and MultiPolygon.
    * each feature has a 'times' property with the same length as the
      coordinates array.
    * each element of each 'times' property is a timestamp in ms since epoch,
      or in ISO string.

    Eventually, you may have Point features with a 'times' property being an
    array of length 1.

    Parameters
    ----------
    data: file, dict or str.
        The timestamped geo-json data you want to plot.

        * If file, then data will be read in the file and fully embedded in
          Leaflet's javascript.
        * If dict, then data will be converted to json and embedded in the
          javascript.
        * If str, then data will be passed to the javascript as-is.
    transition_time: int, default 200.
        The duration in ms of a transition from between timestamps.
    loop: bool, default True
        Whether the animation shall loop.
    auto_play: bool, default True
        Whether the animation shall start automatically at startup.
    add_last_point: bool, default True
        Whether a point is added at the last valid coordinate of a LineString.
    period: str, default "P1D"
        Used to construct the array of available times starting
        from the first available time. Format: ISO8601 Duration
        ex: 'P1M' 1/month, 'P1D' 1/day, 'PT1H' 1/hour, and 'PT1M' 1/minute
    duration: str, default None
        Period of time which the features will be shown on the map after their
        time has passed. If None, all previous times will be shown.
        Format: ISO8601 Duration
        ex: 'P1M' 1/month, 'P1D' 1/day, 'PT1H' 1/hour, and 'PT1M' 1/minute

    Examples
    --------
    >>> TimestampedGeoJson({
    ...     'type': 'FeatureCollection',
    ...     'features': [
    ...       {
    ...         'type': 'Feature',
    ...         'geometry': {
    ...           'type': 'LineString',
    ...           'coordinates': [[-70,-25],[-70,35],[70,35]],
    ...           },
    ...         'properties': {
    ...           'times': [1435708800000, 1435795200000, 1435881600000]
    ...           }
    ...         }
    ...       ]
    ...     })

    See https://github.com/socib/Leaflet.TimeDimension for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
                _getDisplayDateFormat: function(date){
                    var newdate = new moment(date);
                    console.log(newdate)
                    return newdate.format("{{this.date_options}}");
                }
            });
            {{this._parent.get_name()}}.timeDimension = L.timeDimension(
                {
                    period: {{ this.period|tojson }},
                }
            );
            var timeDimensionControl = new L.Control.TimeDimensionCustom(
                {{ this.options|tojson }}
            );
            {{this._parent.get_name()}}.addControl(this.timeDimensionControl);

            var geoJsonLayer = L.geoJson({{this.data}}, {
                    pointToLayer: function (feature, latLng) {
                        if (feature.properties.icon == 'marker') {
                            if(feature.properties.iconstyle){
                                return new L.Marker(latLng, {
                                    icon: L.icon(feature.properties.iconstyle)});
                            }
                            //else
                            return new L.Marker(latLng);
                        }
                        if (feature.properties.icon == 'circle') {
                            if (feature.properties.iconstyle) {
                                return new L.circleMarker(latLng, feature.properties.iconstyle)
                                };
                            //else
                            return new L.circleMarker(latLng);
                        }
                        //else

                        return new L.Marker(latLng);
                    },
                    style: function (feature) {
                        return feature.properties.style;
                    },
                    onEachFeature: function(feature, layer) {
                        if (feature.properties.popup) {
                        layer.bindPopup(feature.properties.popup);
                        }
                    }
                })

            var {{this.get_name()}} = L.timeDimension.layer.geoJson(
                geoJsonLayer,
                {
                    updateTimeDimension: true,
                    addlastPoint: {{ this.add_last_point|tojson }},
                    duration: {{ this.duration }},
                }
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)  # noqa

    def __init__(self, data, transition_time=200, loop=True, auto_play=True,
                 add_last_point=True, period='P1D', min_speed=0.1, max_speed=10,
                 loop_button=False, date_options='YYYY-MM-DD HH:mm:ss',
                 time_slider_drag_update=False, duration=None):
        super(TimestampedGeoJson, self).__init__()
        self._name = 'TimestampedGeoJson'

        if 'read' in dir(data):
            self.embed = True
            self.data = data.read()
        elif type(data) is dict:
            self.embed = True
            self.data = json.dumps(data)
        else:
            self.embed = False
            self.data = data
        self.add_last_point = bool(add_last_point)
        self.period = period
        self.date_options = date_options
        self.duration = 'undefined' if duration is None else '"' + duration + '"'

        self.options = parse_options(
            position='bottomleft',
            min_speed=min_speed,
            max_speed=max_speed,
            auto_play=auto_play,
            loop_button=loop_button,
            time_slider_drag_update=time_slider_drag_update,
            player_options={
                'transitionTime': int(transition_time),
                'loop': loop,
                'startOver': True
            },
        )

    def render(self, **kwargs):
        assert isinstance(self._parent, Map), (
            'TimestampedGeoJson can only be added to a Map object.'
        )
        super(TimestampedGeoJson, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js'),  # noqa
            name='jquery2.0.0')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js'),  # noqa
            name='jqueryui1.10.2')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/nezasa/iso8601-js-period/master/iso8601.min.js'),  # noqa
            name='iso8601')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js'),  # noqa
            name='leaflet.timedimension')

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css'),  # noqa
            name='highlight.js_css')

        figure.header.add_child(
            CssLink("https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.control.min.css"),  # noqa
            name='leaflet.timedimension_css')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js'),
            name='moment')

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
