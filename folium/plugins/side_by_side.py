# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
import json

from branca.element import Figure, JavascriptLink, MacroElement
from jinja2 import Template
from folium.raster_layers import TileLayer, WmsTileLayer

class SideBySide(MacroElement):
    """Add a side-by-side control to an existing map.

    Uses the Leaflet plugin by Digidem under MIT License.
    https://github.com/digidem/leaflet-side-by-side

    Parameters
    ----------
    left_layer : folium TileLayer or WMSTileLayer
        A layer to show on the left side of the map. Any layer added to the map 
        that is here will be shown on the left.
    right_layer : folium TileLayer or WMSTileLayer
        A layer to show on the right side of the map. Any layer added to the 
        map that is here will be shown on the right. This should not be the 
        same as any layer in `left_layers`.
    version : str, default None
        The version of the javascript library to use. Default value will use 
        the development version. Valid values are None, 'gh-pages', 'v2.0.0', 
        'v1.1.1', 'v1.1.0', 'v1.0.2' or 'v1.0.1'.

    Examples
    --------
    >>> m = folium.Map(location=[40, 0], zoom_start=12, tiles='Stamen Terrain')
    >>> left_layer = folium.CircleMarker(
    ...     location=[40, -1], 
    ...     radius=500
    ... ).add_to(m)
    >>> right_layer = folium.CircleMarker(
    ...     location=[40, 1], 
    ...     radius=500
    ... ).add_to(m)
    >>> sbs = SideBySide(left_layer, right_layer)
    >>> m.add_child(sbs)
    """

    _template = Template("""
        {% macro script(this, kwargs) %}

            var {{this.get_name()}} = new L.Control.SideBySide(
            {{this.left_layer.get_name()}}, {{this.right_layer.get_name()}});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
    """)  # noqa

    def __init__(self, left_layer, right_layer, version=None):

        super(SideBySide, self).__init__()
        self._name = 'SideBySide'
        # Check input layers
        if not isinstance(left_layer, (TileLayer, WmsTileLayer)):
            raise TypeError('"left_layer" shall be a folium TileLayer or '
                            'WmsTileLayer instance.')
        if not isinstance(right_layer, (TileLayer, WmsTileLayer)):
            raise TypeError('"right_layer" shall be a folium TileLayer or '
                            'WmsTileLayer instance.')
        self.left_layer = left_layer
        self.right_layer = right_layer
        # Manage version
        versions = ('gh-pages', 'v2.0.0', 'v1.1.1', 
                    'v1.1.0', 'v1.0.2', 'v1.0.1')
        if not version:
            version = versions[0]
        if version in versions:
            self._jslink = ('https://rawcdn.githack.com/digidem/'
                            'leaflet-side-by-side/{}/'
                            'leaflet-side-by-side.js').format(version)
        else:
            raise ValueError('"version" is not a valid value.')
        

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        super(SideBySide, self).render()

        figure.header.add_child(JavascriptLink(self._jslink))  # noqa
