# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
import json

from branca.element import Figure, JavascriptLink, MacroElement

from folium.folium import Map
from folium.utilities import get_obj_in_upper_tree

from jinja2 import Template


class StripePattern(MacroElement):
    """Fill Pattern for polygon composed of alternating lines.

    Add these to the 'fillPattern' field in GeoJson style functions.

    Parameters
    ----------
    angle: float, default 0.5
        Angle of the line pattern (degrees). Should be between -360 and 360.
    weight: float, default 4
        Width of the main lines (pixels).
    space_weight: float
        Width of the alternate lines (pixels).
    color: string with hexadecimal, RGB, or named color, default "#000000"
        Color of the main lines.
    space_color: string with hexadecimal, RGB, or named color, default "#ffffff"
        Color of the alternate lines.
    opacity: float, default 0.75
        Opacity of the main lines. Should be between 0 and 1.
    space_opacity: float, default 0.0
        Opacity of the alternate lines. Should be between 0 and 1.

    See https://github.com/teastman/Leaflet.pattern for more information.
    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = new L.StripePattern(
            {{ this.options }}
        );
        {{ this.get_name() }}.addTo({{ this.parent_map.get_name() }});
        {% endmacro %}
    """)

    def __init__(self, angle=.5, weight=4, space_weight=4,
                 color="#000000", space_color="#ffffff",
                 opacity=0.75, space_opacity=0.0):
        super(StripePattern, self).__init__()
        self._name = 'StripePattern'
        self.options = json.dumps({
            'angle': angle,
            'weight': weight,
            'spaceWeight': space_weight,
            'color': color,
            'spaceColor': space_color,
            'opacity': opacity,
            'spaceOpacity': space_opacity
        })
        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        super(StripePattern, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js'),  # noqa
            name='pattern'
        )


class CirclePattern(MacroElement):
    """Fill Pattern for polygon composed of repeating circles.

    Add these to the 'fillPattern' field in GeoJson style functions.

    Parameters
    ----------
    width: int, default 20
        Horizontal distance between circles (pixels).
    height: int, default 20
        Vertical distance between circles (pixels).
    radius: int, default 12
        Radius of each circle (pixels).
    weight: float, default 2.0
        Width of outline around each circle (pixels).
    color: string with hexadecimal, RGB, or named color, default "#3388ff"
        Color of the circle outline.
    fill_color: string with hexadecimal, RGB, or named color, default "#3388ff"
        Color of the circle interior.
    opacity: float, default 0.75
        Opacity of the circle outline. Should be between 0 and 1.
    fill_opacity: float, default 0.5
        Opacity of the circle interior. Should be between 0 and 1.

    See https://github.com/teastman/Leaflet.pattern for more information.
    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var shape = new L.PatternCircle(
            {{ this.options_pattern_circle }}
        );
        var {{this.get_name()}} = new L.Pattern(
            {{ this.options_pattern }}
        );
        {{ this.get_name() }}.addShape(shape);
        {{ this.get_name() }}.addTo({{ this.parent_map }});
        {% endmacro %}
    """)

    def __init__(self, width=20, height=20, radius=12, weight=2.0,
                 color="#3388ff", fill_color="#3388ff",
                 opacity=0.75, fill_opacity=0.5):
        super(CirclePattern, self).__init__()
        self._name = 'CirclePattern'
        self.options_pattern_circle = json.dumps({
            'x': radius + 2 * weight,
            'y': radius + 2 * weight,
            'weight': weight,
            'radius': radius,
            'color': color,
            'fillColor': fill_color,
            'opacity': opacity,
            'fillOpacity': fill_opacity,
            'fill': True,
        })
        self.options_pattern = json.dumps({
            'width': width,
            'height': height,
        })
        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map).get_name()
        super(CirclePattern, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js'),  # noqa
            name='pattern'
        )
