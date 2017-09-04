# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import CssLink, Figure, JavascriptLink

from folium.map import Icon, Layer, Marker, Popup

from jinja2 import Template


class MarkerCluster(Layer):
    """
    Provides Beautiful Animated Marker Clustering functionality for maps.

    Parameters
    ----------
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls
    icon_create_function : string, default None
        Override the default behaviour, making possible to customize
        markers colors and sizes.

    locations: list of list or array of shape (n, 2).
        Data points of the form [[lat, lng]].
    popups: list of length n.
        Popup for each marker.
    icons: list of length n.
        Icon for each marker.

    Example
    -------
    >>> icon_create_function = '''
    ...    function(cluster) {
    ...    return L.divIcon({html: '<b>' + cluster.getChildCount() + '</b>',
    ...                      className: 'marker-cluster marker-cluster-small',
    ...                      iconSize: new L.Point(20, 20)});
    }'''

    """
    def __init__(self, locations=None, popups=None, icons=None, name=None,
                 overlay=True, control=True, icon_create_function=None):
        super(MarkerCluster, self).__init__(name=name, overlay=overlay, control=control)  # noqa

        if locations is not None:
            if popups is None:
                popups = [None]*len(locations)
            if icons is None:
                icons = [None]*len(locations)
            for location, popup, icon in zip(locations, popups, icons):
                p = popup if popup is None or isinstance(popup, Popup) else Popup(popup)  # noqa
                i = icon if icon is None or isinstance(icon, Icon) else Icon(icon)  # noqa
                self.add_child(Marker(location, popup=p, icon=i))

        self._name = 'MarkerCluster'
        self._icon_create_function = icon_create_function.strip() if icon_create_function else ''  # noqa
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.markerClusterGroup({
                {% if this._icon_create_function %}
                   iconCreateFunction: {{this._icon_create_function}}
                {% endif %}
            });
            {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(MarkerCluster, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js'),  # noqa
            name='markerclusterjs')

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css'),  # noqa
            name='markerclustercss')

        figure.header.add_child(
            CssLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css'),  # noqa
            name='markerclusterdefaultcss')
