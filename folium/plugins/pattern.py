from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.folium import Map
from folium.utilities import get_obj_in_upper_tree, parse_options

from jinja2 import Template


class StripePattern(JSCSSMixin, MacroElement):
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
                {{ this.options|tojson }}
            );
            {{ this.get_name() }}.addTo({{ this.parent_map.get_name() }});
        {% endmacro %}
    """)

    default_js = [
        ('pattern',
         'https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js')
    ]

    def __init__(self, angle=.5, weight=4, space_weight=4,
                 color="#000000", space_color="#ffffff",
                 opacity=0.75, space_opacity=0.0, **kwargs):
        super(StripePattern, self).__init__()
        self._name = 'StripePattern'
        self.options = parse_options(
            angle=angle,
            weight=weight,
            space_weight=space_weight,
            color=color,
            space_color=space_color,
            opacity=opacity,
            space_opacity=space_opacity,
            **kwargs
        )
        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        super(StripePattern, self).render(**kwargs)


class CirclePattern(JSCSSMixin, MacroElement):
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
            var {{ this.get_name() }}_shape = new L.PatternCircle(
                {{ this.options_pattern_circle|tojson }}
            );
            var {{ this.get_name() }} = new L.Pattern(
                {{ this.options_pattern|tojson }}
            );
            {{ this.get_name() }}.addShape({{ this.get_name() }}_shape);
            {{ this.get_name() }}.addTo({{ this.parent_map }});
        {% endmacro %}
    """)

    default_js = [
        ('pattern',
         'https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js')
    ]

    def __init__(self, width=20, height=20, radius=12, weight=2.0,
                 color="#3388ff", fill_color="#3388ff",
                 opacity=0.75, fill_opacity=0.5):
        super(CirclePattern, self).__init__()
        self._name = 'CirclePattern'
        self.options_pattern_circle = parse_options(
            x=radius + 2 * weight,
            y=radius + 2 * weight,
            weight=weight,
            radius=radius,
            color=color,
            fill_color=fill_color,
            opacity=opacity,
            fill_opacity=fill_opacity,
            fill=True,
        )
        self.options_pattern = parse_options(
            width=width,
            height=height,
        )
        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map).get_name()
        super(CirclePattern, self).render(**kwargs)
