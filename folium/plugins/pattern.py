# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import Figure, JavascriptLink, MacroElement

from jinja2 import Template


class StripePattern(MacroElement):
    """
    Fill Pattern for polygon composed of alternating lines

    Parameters
    ----------
    angle: int -360-360
        angle of the line pattern (degrees).

    weight: float
        width of the main lines (pixels).

    space_weight: float
        width of the alternate lines (pixels).

    width: int
        Horizontal distance between circles (pixels).

    color: string with hexadecimal, RGB, or named color, default "#000000"
        color of the main lines.

    space_color: string with hexadecimal, RGB, or named color, default "#ffffff"
        color of the alternate lines.

    opacity: float 0.0-1.0, default 0.75
        opacity of the main lines.

    space_opacity: float 0.0-1.0, default 0.0
        opacity of the alternate lines.

    See https://github.com/teastman/Leaflet.pattern for more information.

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new L.StripePattern({
                                                            angle: {{this.angle}},
                                                            weight: {{this.weight}},
                                                            spaceWeight: {{this.space_weight}},
                                                            color: "{{this.color}}",
                                                            spaceColor: "{{this.space_color}}",
                                                            opacity: {{this.opacity}},
                                                            spaceOpacity: {{this.space_opacity}}
                                                          });
            {{this.get_name()}}.addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, angle=.5, weight=4, space_weight=4,
                 color="#000000", space_color="#ffffff",
                 opacity=0.75, space_opacity=0.0, **kwargs):
        super(StripePattern, self).__init__()
        self._name = 'StripePattern'
        self.angle = angle
        self.weight = weight
        self.space_weight = space_weight
        self.color = color
        self.space_color = space_color
        self.opacity = opacity
        self.space_opacity = space_opacity

    def render(self, **kwargs):
        super(StripePattern, self).render(angle=self.angle,
                                          weight=self.weight,
                                          space_weight=self.space_weight,
                                          color=self.color,
                                          space_color=self.space_color,
                                          opacity=self.opacity,
                                          space_opacity=self.space_opacity,
                                          **kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js'),  # noqa
            name='pattern')


class CirclePattern(MacroElement):
    """
    Fill Pattern for polygon composed of repeating circles

    Parameters
    ----------
    weight: float
        width of outline around each circle (pixels).

    radius: int
        radius of each circle (pixels).

    width: int
        Horizontal distance between circles (pixels).

    height: int
        Vertical distance between circles (pixels).

    color: string with hexadecimal, RGB, or named color, default "#3388ff"
        color of the circle outline.

    fill_color: string with hexadecimal, RGB, or named color, default "#3388ff"
        color of the circle interior.

    opacity: float 0.0-1.0, default 0.75
        opacity of the circle outline.

    fill_opacity: float 0.0-1.0, default 0.5
        opacity of the circle interior.

    See https://github.com/teastman/Leaflet.pattern for more information.
    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
            var shape = new L.PatternCircle({
                x: {{this.radius + 2 * this.weight}},
                y: {{this.radius + 2 * this.weight}},
                weight: {{this.weight}},
                radius: {{this.radius}},
                color: "{{this.color}}",
                fillColor: "{{this.fill_color}}",
                opacity: {{this.opacity}},
                fillOpacity: {{this.fill_opacity}},
                fill: true
            });

            var {{this.get_name()}} = new L.Pattern({width:{{this.width}}, height:{{this.height}}});
            {{this.get_name()}}.addShape(shape);
            {{this.get_name()}}.addTo({{this._parent.get_name()}});

            {% endmacro %}
            """)

    def __init__(self, width=20, height=20, radius=12,
                 weight=2,
                 color="#3388ff", fill_color="#3388ff",
                 opacity=0.75, fill_opacity=0.5, **kwargs):
        super(CirclePattern, self).__init__()
        self._name = 'CirclePattern'
        self.width = width
        self.height = height
        self.radius = radius
        self.weight = weight
        self.color = color
        self.fill_color = fill_color
        self.opacity = opacity
        self.fill_opacity = fill_opacity

    def render(self, **kwargs):
        super(CirclePattern, self).render(radius=self.radius,
                                          width=self.width,
                                          height=self.height,
                                          weight=self.weight,
                                          color=self.color,
                                          fill_color=self.fill_color,
                                          opacity=self.opacity,
                                          fill_opacity=self.fill_opacity,
                                          **kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js'),  # noqa
            name='pattern')
