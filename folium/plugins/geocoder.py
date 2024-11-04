from typing import Optional

from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template


class Geocoder(JSCSSMixin, MacroElement):
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
    zoom: int, default 11, optional
        Set zoom level used for displaying the geocode result, note that this only has an effect when add_marker is set to False. Set this to None to preserve the current map zoom level.
    provider: str, default 'nominatim'
        Defaults to "nominatim", see https://github.com/perliedman/leaflet-control-geocoder/tree/2.4.0/src/geocoders for other built-in providers.
    provider_options: dict, default {}
        For use with specific providers that may require api keys or other parameters.

    For all options see https://github.com/perliedman/leaflet-control-geocoder

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}

            var geocoderOpts_{{ this.get_name() }} = {{ this.options|tojavascript }};

            // note: geocoder name should start with lowercase
            var geocoderName_{{ this.get_name() }} = geocoderOpts_{{ this.get_name() }}["provider"];

            var customGeocoder_{{ this.get_name() }} = L.Control.Geocoder[ geocoderName_{{ this.get_name() }} ](
                geocoderOpts_{{ this.get_name() }}['providerOptions']
            );
            geocoderOpts_{{ this.get_name() }}["geocoder"] = customGeocoder_{{ this.get_name() }};

            L.Control.geocoder(
                geocoderOpts_{{ this.get_name() }}
            ).on('markgeocode', function(e) {
                var zoom = geocoderOpts_{{ this.get_name() }}['zoom'] || {{ this._parent.get_name() }}.getZoom();
                {{ this._parent.get_name() }}.setView(e.geocode.center, zoom);
            }).addTo({{ this._parent.get_name() }});

        {% endmacro %}
    """
    )

    default_js = [
        (
            "Control.Geocoder.js",
            "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js",
        )
    ]
    default_css = [
        (
            "Control.Geocoder.css",
            "https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css",
        )
    ]

    def __init__(
        self,
        collapsed: bool = False,
        position: str = "topright",
        add_marker: bool = True,
        zoom: Optional[int] = 11,
        provider: str = "nominatim",
        provider_options: dict = {},
        **kwargs
    ):
        super().__init__()
        self._name = "Geocoder"
        self.options = dict(
            collapsed=collapsed,
            position=position,
            default_mark_geocode=add_marker,
            zoom=zoom,
            provider=provider,
            provider_options=provider_options,
            **kwargs
        )
