from folium.elements import JSCSSMixin
from folium.map import Marker
from folium.utilities import parse_options

from jinja2 import Template


class BoatMarker(JSCSSMixin, Marker):
    """Add a Marker in the shape of a boat.

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

    https://github.com/thomasbrueggemann/leaflet.boatmarker

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.boatMarker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
            {% if this.wind_heading is not none -%}
            {{ this.get_name() }}.setHeadingWind(
                {{ this.heading }},
                {{ this.wind_speed }},
                {{ this.wind_heading }}
            );
            {% else -%}
            {{this.get_name()}}.setHeading({{this.heading}});
            {% endif -%}
        {% endmacro %}
        """)

    default_js = [
        ('markerclusterjs',
         'https://unpkg.com/leaflet.boatmarker/leaflet.boatmarker.min.js'),
    ]

    def __init__(self, location, popup=None, icon=None,
                 heading=0, wind_heading=None, wind_speed=0, **kwargs):
        super(BoatMarker, self).__init__(
            location,
            popup=popup,
            icon=icon
        )
        self._name = 'BoatMarker'
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.options = parse_options(**kwargs)
