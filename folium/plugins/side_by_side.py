from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer


class SideBySideLayers(JSCSSMixin, Layer):
    """
    Creates a SideBySideLayers that takes two Layers and adds a sliding
    control with the leaflet-side-by-side plugin.

    Uses the Leaflet leaflet-side-by-side plugin https://github.com/digidem/leaflet-side-by-side

    Parameters
    ----------
    layer_left: Layer.
        The left Layer within the side by side control.
        Must be created and added to the map before being passed to this class.
    layer_right: Layer.
        The right Layer within the side by side control.
        Must be created and added to the map before being passed to this class.

    Examples
    --------
    >>> sidebyside = SideBySideLayers(layer_left, layer_right)
    >>> sidebyside.add_to(m)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.control.sideBySide(
                {{ this.layer_left.get_name() }}, {{ this.layer_right.get_name() }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    default_js = [
        (
            "leaflet.sidebyside",
            "https://cdn.jsdelivr.net/gh/digidem/leaflet-side-by-side@gh-pages/leaflet-side-by-side.min.js",
        ),
    ]

    def __init__(self, layer_left, layer_right):
        super().__init__(control=False)
        self._name = "SideBySideLayers"
        self.layer_left = layer_left
        self.layer_right = layer_right
