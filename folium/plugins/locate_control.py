"""Add Locate control to folium Map.

Based on leaflet plugin: https://github.com/domoritz/leaflet-locatecontrol
"""

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class LocateControl(MacroElement):
    """Control plugin to geolocate the user.

    Parameters
    ----------
    options: dict, optional
        For possible options, see https://github.com/domoritz/leaflet-locatecontrol

    Examples
    --------
    >>> import folium
    >>> from folium.plugins import LocateControl
    >>> map = folium.Map()
    # With default settings
    >>> LocateControl().add_to(map)

    # With custom options
    >>> options = {"position": "topright",
    ...             "strings":{
    ...                     "title":"Show my current location"}}
    >>> LocateControl(options=options).add_to(map)

    For more info check:
    https://github.com/domoritz/leaflet-locatecontrol

    """

    _template = Template(u"""
                         {% macro script(this, kwargs) %}
                         var {{this.get_name()}} = L.control.locate(
                                        {{this.options|tojson}}).addTo({{this._parent.get_name()}});
                         {% endmacro %}
                         """)

    def __init__(self, options=None):
        """Initialization."""
        super(LocateControl, self).__init__()
        self._name = 'LocateControl'
        self.options = options or {}

    def render(self, **kwargs):
        super(LocateControl, self).render(**kwargs)
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            CssLink(
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.css"))  # noqa
        figure.header.add_child(JavascriptLink(
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.js"))  # noqa
