from branca.element import CssLink, Figure, JavascriptLink, MacroElement
from jinja2 import Template

from folium.utilities import parse_options


class Geocoder(MacroElement):
    """A simple geocoder for Leaflet that by default uses OSM/Nominatim.

    Please respect the Nominatim usage policy:
    https://operations.osmfoundation.org/policies/nominatim/

    Parameters
    ----------
    collapsed: bool, default False
        If True, collapses the search box unless hovered/clicked.
    position: str, default 'topright'
        Choose from 'topleft', 'topright', 'bottomleft' or 'bottomright'.
    add_marker: bool, default True
        If True, adds a marker on the found location.

    For all options see https://github.com/perliedman/leaflet-control-geocoder

    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
            L.Control.geocoder(
                {{ this.options|tojson }}
            ).on('markgeocode', function(e) { 
                {{ this._parent.get_name() }}.setView(e.geocode.center, 11);
            }).addTo({{ this._parent.get_name() }});

        {% endmacro %}
    """)

    def __init__(
            self,
            collapsed=False,
            position='topright',
            add_marker=True,
            **kwargs
    ):
        super(Geocoder, self).__init__()
        self._name = 'Geocoder'
        self.options = parse_options(
            collapsed=collapsed,
            position=position,
            defaultMarkGeocode=add_marker,
            **kwargs
        )

    def render(self, **kwargs):
        super(Geocoder, self).render(**kwargs)
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(CssLink(
            "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css"))  # noqa
        figure.header.add_child(JavascriptLink(
            "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"))  # noqa
