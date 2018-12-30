# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import json

from branca.element import CssLink, Figure, JavascriptLink

from folium.map import Icon, Layer, Marker, Popup

from jinja2 import Template


class MarkerCluster(Layer):
    """
    Provides Beautiful Animated Marker Clustering functionality for maps.

    Parameters
    ----------
    locations: list of list or array of shape (n, 2).
        Data points of the form [[lat, lng]].
    popups: list of length n, default None
        Popup for each marker, either a Popup object or a string or None.
    icons: list of length n, default None
        Icon for each marker, either an Icon object or a string or None.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    icon_create_function : string, default None
        Override the default behaviour, making possible to customize
        markers colors and sizes.
    options : dict, default None
        A dictionary with options for Leaflet.markercluster. See
        https://github.com/Leaflet/Leaflet.markercluster for options.

    Example
    -------
    >>> icon_create_function = '''
    ...     function(cluster) {
    ...     return L.divIcon({html: '<b>' + cluster.getChildCount() + '</b>',
    ...                       className: 'marker-cluster marker-cluster-small',
    ...                       iconSize: new L.Point(20, 20)});
    ...     }
    ... '''

    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.markerClusterGroup({{ this.options }});
            {%- if this.icon_create_function is not none %}
            {{ this.get_name() }}.options.iconCreateFunction =
                {{ this.icon_create_function.strip() }};
            {%- endif %}
            {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)

    def __init__(self, locations=None, popups=None, icons=None, name=None,
                 overlay=True, control=True, show=True,
                 icon_create_function=None, options=None):
        super(MarkerCluster, self).__init__(name=name, overlay=overlay,
                                            control=control, show=show)
        self._name = 'MarkerCluster'

        if locations is not None:
            if popups is None:
                popups = [None] * len(locations)
            if icons is None:
                icons = [None] * len(locations)
            for location, popup, icon in zip(locations, popups, icons):
                p = popup if self._validate(popup, Popup) else Popup(popup)
                i = icon if self._validate(icon, Icon) else Icon(icon)
                self.add_child(Marker(location, popup=p, icon=i))

        options = {} if options is None else options
        self.options = json.dumps(options, sort_keys=True, indent=2)
        if icon_create_function is not None:
            assert isinstance(icon_create_function, str)
        self.icon_create_function = icon_create_function

    @staticmethod
    def _validate(obj, cls):
        """Check whether the given object is from the given class or is None."""
        return True if obj is None or isinstance(obj, cls) else False

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
