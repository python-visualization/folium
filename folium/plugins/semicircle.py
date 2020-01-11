# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import Figure, JavascriptLink

from folium.map import Marker
from folium.utilities import _validate_location

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

    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                if ({{this.direction}} || {{this.arc}}) {
                    var {{this.get_name()}} = L.semiCircle(
                        [{{this.location[0]}},{{this.location[1]}}],
                        {radius:{{this.radius}},
                        fill: {{this.fill}},
                        fillColor:'{{this.fill_color}}',
                        fillOpacity: {{this.fill_opacity}},
                        color: '{{this.color}}',
                        opacity: {{this.opacity}}
                        }).setDirection({{this.direction}},{{this.arc}})
                        .addTo({{this._parent.get_name()}});
                } else if ({{this.start_angle}} || {{this.stop_angle}}) {
                    var {{this.get_name()}} = L.semiCircle(
                        [{{this.location[0]}},{{this.location[1]}}],
                        {radius:{{this.radius}},
                        fill: {{this.fill}},
                        fillColor:'{{this.fill_color}}',
                        fillOpacity: {{this.fill_opacity}},
                        color: '{{this.color}}',
                        opacity: {{this.opacity}},
                        startAngle:{{this.start_angle}},
                        stopAngle:{{this.stop_angle}}
                        })
                        .addTo({{this._parent.get_name()}});
                }
            {% endmacro %}
            """)

    def __init__(self, location, radius, direction=None, arc=None, start_angle=None, stop_angle=None, fill=True,
                 fill_color='#3388ff', fill_opacity=0.5, color='#3388ff', opacity=1, **kwargs):
        super(SemiCircle, self).__init__(_validate_location(location), **kwargs)
        self._name = 'SemiCircle'
        self.radius = radius
        self.direction = json.dumps(direction)
        self.arc = json.dumps(arc)
        self.start_angle = json.dumps(start_angle)
        self.stop_angle = json.dumps(stop_angle)
        if fill:
            self.fill = 'true'
        else:
            self.fill = 'false'
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.color = color
        self.opacity = opacity
        self.kwargs = json.dumps(kwargs)

        if not ((direction is None and arc is None) and (start_angle is not None and stop_angle is not None)
                or (direction is not None and arc is not None) and (start_angle is None and stop_angle is None)):
            raise ValueError("Invalid arguments. Either provide direction and arc OR start_angle and stop_angle")

    def render(self, **kwargs):
        super(SemiCircle, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-semicircle@2.0.2/Semicircle.min.js'),
            name='semicirclejs')
