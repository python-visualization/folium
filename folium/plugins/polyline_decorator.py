from folium.elements import JSCSSMixin
from folium.features import MacroElement
from folium.template import Template, tojavascript
from folium.utilities import JsCode


class PolyLineDecorator(JSCSSMixin, MacroElement):
    """
    Draws patterns of symbols, such as arrowheads or dashes, along a line.

    Parameters
    ----------
    polyline: folium.PolyLine or folium.Polygon
        The line to decorate.
    patterns: list of dict
        Each pattern has a ``symbol`` and optionally ``offset``, ``end_offset``
        and ``repeat``, in pixels or as a percentage string such as "10%".
        The ``symbol`` is a dict with a ``type`` of "arrowHead", "dash" or
        "marker", and the options of that symbol, for example
        ``{"type": "arrowHead", "pixel_size": 15, "path_options": {"color": "red"}}``.

    See https://github.com/bbecquet/Leaflet.PolylineDecorator for the options.

    """

    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.polylineDecorator(
                {{ this.polyline.get_name() }},
                {{ this.options|tojavascript }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    default_js = [
        (
            "polylinedecorator",
            "https://cdn.jsdelivr.net/npm/leaflet-polylinedecorator@1.6.0/dist/leaflet.polylineDecorator.min.js",
        )
    ]

    symbol_types = {"arrowHead", "dash", "marker"}

    def __init__(self, polyline, patterns, **kwargs):
        super().__init__()
        self._name = "PolyLineDecorator"
        self.polyline = polyline
        self.options = {
            "patterns": [self._to_pattern(pattern) for pattern in patterns],
            **kwargs,
        }

    def _to_pattern(self, pattern):
        pattern = dict(pattern)
        symbol = dict(pattern["symbol"])
        symbol_type = symbol.pop("type")
        if symbol_type not in self.symbol_types:
            raise ValueError(
                f"symbol type should be one of {sorted(self.symbol_types)}, "
                f"got {symbol_type!r}"
            )
        pattern["symbol"] = JsCode(f"L.Symbol.{symbol_type}({tojavascript(symbol)})")
        return pattern
