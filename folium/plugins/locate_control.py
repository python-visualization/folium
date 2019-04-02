"""Add Locate control to folium Map.

Based on leaflet plugin: https://github.com/domoritz/leaflet-locatecontrol
"""

from __future__ import (absolute_import, division, print_function)
from branca.element import MacroElement, Figure, JavascriptLink, CssLink
from jinja2 import Template


class LocateControl(MacroElement):
    """LocateControl."""

    _template = Template(u"""
                         {% macro script(this, kwargs) %}
                         var {{this.get_name()}} = L.control.locate({
                            strings: {
                              title: "Show me where I am, yo!"
                            }
                          }).addTo({{this._parent.get_name()}});
                         {% endmacro %}
                         """)

    def __init__(self):
        """Initialization."""
        super(LocateControl, self).__init__()
        self._name = "LocateControl"

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
