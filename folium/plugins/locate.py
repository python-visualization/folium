# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import Figure, MacroElement
from jinja2 import Template
from folium import Popup


class Locate(MacroElement):
    """
    Fontawesome icons: https://fontawesome.com/v4.7.0/icons/.

    https://leafletjs.com/reference-1.4.0.html#locate-options

    Parameters
    ----------
    icon: Icon plugin
        the Icon plugin to use to render the marker.
    popup: string, default: "Your current location"
        Label for the Marker; only strings are valid.
    show: bool, default True
        True renders the popup open on page load.

    Examples
    --------
    >>> import folium
    >>> from folium.plugins import Locate
    >>> map = folium.Map()
    # with default values
    >>> Locate().add_to(map)
    # with custom values
    >>>Locate(icon=folium.Icon(icon="fa-ship", prefix='fa'),
           popup="Sua actual localização", show=False).add_to(map)
    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
                function onLocationFound(e) {
                    var {{this.get_name()}} = L.marker(e.latlng).addTo({{this._parent.get_name()}})
                     .bindPopup("{{this.popup}}"){% if this.show%}.openPopup(){% endif %};
                    {% if this.icon != None %}{{this.icon}}{% endif %}
                }
                function onLocationError(e) {
                  alert(e.message);
                }
                {{this._parent.get_name()}}.on(
                    'locationfound', onLocationFound);
                {{this._parent.get_name()}}.on(
                    'locationerror', onLocationError);

                {{this._parent.get_name()}}.locate(
                {setView: true, maxZoom: 16})
            {% endmacro %}
            """)

    def __init__(self, icon=None, popup=None, show=True):
        """Initialization."""
        super(Locate, self).__init__()
        self._name = 'Locate'
        self.show = show
        if icon:
            self.icon = self.custom_icon(icon)

        if popup is None:
            self.popup = "Your current location"
        elif not isinstance(popup, Popup):
            self.popup = popup
        else:
            raise TypeError("Popup can only be a string, not a folium.Popup")

    def custom_icon(self, icon):
        """Create a custom icon from folium.Icon.

        This method generates a figure transforming the folium.Icon in plain javascript in order to
        be able to place the new icon inside the function onLocationFound().
        """
        figure = Figure()
        figure.script.add_child(icon)
        # Iterates over the figure.script.render: First render returns None and the second the Icon
        for i in range(2):
            _string_icon = figure.script.render()
        # Gets current icon parent name. At the moment the parent name is folium.Map
        _icon = icon._parent.get_name()
        # Replace parent name to the self making possible change the default icon
        return _string_icon.replace(_icon, self.get_name())
