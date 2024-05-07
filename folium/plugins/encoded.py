from abc import ABC, abstractmethod

from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.features import MacroElement
from folium.vector_layers import path_options


class _BaseFromEncoded(JSCSSMixin, MacroElement, ABC):
    """Base Interface to create folium objects from encoded strings.

    Derived classes must define `_encoding_type` property which returns the string
    representation of the folium object to create from the encoded string.

    Parameters
    ----------
    encoded: str
        The raw encoded string from the Polyline Encoding Algorithm. See:
        https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    **kwargs:
        Object options as accepted by leaflet.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}

            var {{ this.get_name() }} = L.{{ this._encoding_type }}.fromEncoded(
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

    def __init__(self, encoded: str):
        super().__init__()
        self.encoded = encoded

    @property
    @abstractmethod
    def _encoding_type(self) -> str:
        """An abstract getter to return the type of folium object to create."""
        raise NotImplementedError


class PolyLineFromEncoded(_BaseFromEncoded):
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

    def __init__(self, encoded: str, **kwargs):
        self._name = "PolyLineFromEncoded"
        super().__init__(encoded=encoded)
        self.options = path_options(line=True, **kwargs)

    @property
    def _encoding_type(self) -> str:
        """Return the name of folium object created from the encoded."""
        return "Polyline"


class PolygonFromEncoded(_BaseFromEncoded):
    """Create Polygons directly from the encoded string.

    Parameters
    ----------
    encoded: str
        The raw encoded string from the Polyline Encoding Algorithm. See:
        https://developers.google.com/maps/documentation/utilities/polylinealgorithm
    **kwargs:
        Polygon options as accepted by leaflet. See:
        https://leafletjs.com/reference.html#polygon

    Adapted from https://github.com/jieter/Leaflet.encoded

    Examples
    --------
    >>> from folium import Map
    >>> from folium.plugins import PolygonFromEncoded
    >>> m = Map()
    >>> encoded = r"w`j~FpxivO}jz@qnnCd}~Bsa{@~f`C`lkH"
    >>> PolygonFromEncoded(encoded=encoded).add_to(m)
    """

    def __init__(self, encoded: str, **kwargs):
        self._name = "PolygonFromEncoded"
        super().__init__(encoded)
        self.options = path_options(line=True, radius=None, **kwargs)

    @property
    def _encoding_type(self) -> str:
        """Return the name of folium object created from the encoded."""
        return "Polygon"
