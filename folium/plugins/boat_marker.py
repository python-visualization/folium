# -*- coding: utf-8 -*-
"""
Boat marker
-----------

Creates a marker shaped like a boat.
Optionally you can append a wind direction.

"""
import json
from jinja2 import Template

from branca.element import JavascriptLink, Figure
from folium.map import Marker


class BoatMarker(Marker):
    """Adds a BoatMarker layer on the map."""
    def __init__(self, location, popup=None, icon=None,
                 heading=0, wind_heading=None, wind_speed=0, **kwargs):
        """Creates a BoatMarker plugin to append into a map with
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
        super(BoatMarker, self).__init__(location, popup=popup, icon=icon)
        self._name = 'BoatMarker'
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.kwargs = json.dumps(kwargs)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.boatMarker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                {{this.get_name()}}.setHeadingWind({{this.heading}}, {{this.wind_speed}}, {{this.wind_heading}});
            {% endmacro %}
            """)  # noqa

    def render(self, **kwargs):
        super(BoatMarker, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://thomasbrueggemann.github.io/leaflet.boatmarker/js/leaflet.boatmarker.min.js"),  # noqa
            name='markerclusterjs')
