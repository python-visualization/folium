# -*- coding: utf-8 -*-
"""
Marker Cluster plugin
---------------------

Creates a MarkerCluster plugin to add on a folium map.
"""

from jinja2 import Template

from branca.element import JavascriptLink, CssLink, MacroElement, Figure

from folium.map import Popup, Icon, Marker


class MarkerCluster(MacroElement):
    def __init__(self, locations, popups=None, icons=None):
        """Creates a MarkerCluster plugin to append into a map with
        Map.add_child.

        Parameters
        ----------
            locations: list of list or array of shape (n,2).
                Data points of the form [[lat, lng]].

            popups: list of length n.
                Popup for each marker.

            icons: list of length n.
                Icon for each marker.
        """
        super(MarkerCluster, self).__init__()
        self._name = 'MarkerCluster'

        if popups is None:
            popups = [None]*len(locations)
        if icons is None:
            icons = [None]*len(locations)

        for location, popup, icon in zip(locations, popups, icons):
            if popup is None or isinstance(popup, Popup):
                p = popup
            else:
                p = Popup(popup)
            if icon is None or isinstance(icon, Icon):
                i = icon
            else:
                i = Icon(icon)
            self.add_child(Marker(location, popup=p, icon=i))

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.markerClusterGroup();
                {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(MarkerCluster, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/leaflet.markercluster.js"),  # noqa
            name='markerclusterjs')

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/MarkerCluster.css"),  # noqa
            name='markerclustercss')

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.0/MarkerCluster.Default.css"),  # noqa
            name='markerclusterdefaultcss')
