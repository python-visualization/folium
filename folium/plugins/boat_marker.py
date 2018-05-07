# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import Figure, JavascriptLink

from folium.map import Marker
from folium.utilities import _validate_location

from jinja2 import Template


class BoatMarker(Marker):
    """
    Creates a BoatMarker plugin to append into a map with
    Map.add_plugin.

    Parameters
    ----------
    location: tuple of length 2, default None
        The latitude and longitude of the marker.
        If None, then the middle of the map is used.

    heading: int, default 0
        Heading of the boat to an angle value between 0 and 360 degrees

    wind_heading: int, default None
        Heading of the wind to an angle value between 0 and 360 degrees
        If None, then no wind is represented.

    wind_speed: int, default 0
        Speed of the wind in knots.

    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.boatMarker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                {% if this.wind_heading is not none -%}
                {{this.get_name()}}.setHeadingWind({{this.heading}}, {{this.wind_speed}}, {{this.wind_heading}});
                {% else -%}
                {{this.get_name()}}.setHeading({{this.heading}});
                {% endif -%}
            {% endmacro %}
            """)  # noqa

    def __init__(self, location, popup=None, icon=None,
                 heading=0, wind_heading=None, wind_speed=0, **kwargs):
        super(BoatMarker, self).__init__(
            _validate_location(location),
            popup=popup,
            icon=icon
        )
        self._name = 'BoatMarker'
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.kwargs = json.dumps(kwargs)

    def render(self, **kwargs):
        super(BoatMarker, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://unpkg.com/leaflet.boatmarker/leaflet.boatmarker.min.js'),  # noqa
            name='markerclusterjs')
