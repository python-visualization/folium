from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.features import MacroElement
from folium.utilities import parse_options


class PolyLineFromEncoded(JSCSSMixin, MacroElement):
    """Create PolyLines directly from the encoded string.

    Parameters
    ----------
    encoded: str
        The raw encoded string from the Polyline Encoding Algorithm. See:
        https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    **kwargs:
        Polyline options as accepted by leaflet. See:
        https://leafletjs.com/reference.html#polyline

    Adapted from https://github.com/jieter/Leaflet.encoded

    Examples
    --------
    >>> from folium import Map
    >>> from folium.plugins import PolyLineFromEncoded
    >>> m = Map()
    >>> encoded = r"_p~iF~cn~U_ulLn{vA_mqNvxq`@"
    >>> PolyLineFromEncoded(encoded=encoded, color="green").add_to(m)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}

            var {{ this.get_name() }} = L.Polyline.fromEncoded(
                {{ this.encoded|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});

        {% endmacro %}
        """
    )
    default_js = [
        (
            "polyline-encoded",
            "https://cdn.jsdelivr.net/npm/polyline-encoded@0.0.9/Polyline.encoded.js",
        )
    ]

    def __init__(self, encoded, **kwargs):
        super().__init__()
        self._name = "PolyLineFromEncoded"
        self.encoded = encoded
        self.options = parse_options(**kwargs)
