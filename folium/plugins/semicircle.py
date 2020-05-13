# -*- coding: utf-8 -*-

from branca.element import Figure, JavascriptLink

from folium.map import Marker
from folium.utilities import parse_options

from jinja2 import Template


class SemiCircle(Marker):
    """
    Creates a Semicircle plugin to add to a map.
    Use (direction and arc) or (start_angle and stop_angle)
    Parameters
    ----------
    location: tuple of length 2,
        The latitude and longitude of the marker.
        If None, then the middle of the map is used.
    radius: int
        Radius of semicircle in meters
    direction: int, default None
        Heading of direction angle value between 0 and 360 degrees
    arc: int, default None
        Heading of arc angle value between 0 and 360 degrees.
    start_angle: int, default None
        Heading of the start angle value between 0 and 360 degrees
    stop_angle: int, default None
        Heading of the stop angle value between 0 and 360 degrees.
    fill_color: string, default '#3388ff' (blue)
        Fill color
    fill_opacity: float 0-1, default 0.5
        Fill opacity
    color: string, default '#3388ff' (blue)
        Line color
    opacity: float 0-1, default 1
        Line opacity
    **kwargs:
        Passed to Marker so a popup and tooltip can be provided.
    https://github.com/jieter/Leaflet-semicircle
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                    var {{ this.get_name() }} = L.semiCircle(
                        {{ this.location|tojson }},
                        {{ this.options | tojson }}
                        )
                        {% if this.direction %}
                            .setDirection{{ this.direction }}
                        {% endif %}
                        .addTo({{ this._parent.get_name() }});
            {% endmacro %}
            """)

    def __init__(self, location, radius, direction=None, arc=None, start_angle=None, stop_angle=None, fill=True,
                 fill_color='#3388ff', fill_opacity=0.5, color='#3388ff', opacity=1, **kwargs):
        super(SemiCircle, self).__init__(location, **kwargs)
        self._name = 'SemiCircle'
        self.direction = (direction, arc) if direction and arc else None
        self.options = parse_options(
            radius=radius,
            start_angle=start_angle,
            stop_angle=stop_angle,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            color=color,
            opacity=opacity,
            fill='true' if fill else 'false',
            **kwargs
        )

        if not ((direction is None and arc is None) and (start_angle is not None and stop_angle is not None)
                or (direction is not None and arc is not None) and (start_angle is None and stop_angle is None)):
            raise ValueError("Invalid arguments. Either provide direction and arc OR start_angle and stop_angle")

    def render(self, **kwargs):
        super(SemiCircle, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-semicircle@2.0.4/Semicircle.min.js'),
            name='semicirclejs')
