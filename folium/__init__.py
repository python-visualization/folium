# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.colormap import (ColorMap, LinearColormap, StepColormap)
from branca.element import (CssLink, Div, Element, Figure, Html, IFrame,
                            JavascriptLink, Link, MacroElement)

from folium._version import get_versions

from folium.features import (
    ClickForMarker, ColorLine, CustomIcon, DivIcon, GeoJson,
    LatLngPopup, RegularPolygonMarker, TopoJson, Vega, VegaLite,
    GeoJsonTooltip,
)

from folium.raster_layers import TileLayer, WmsTileLayer

from folium.folium import Map

from folium.map import (
    FeatureGroup, FitBounds, Icon, LayerControl, Marker, Popup, Tooltip
)

from folium.vector_layers import Circle, CircleMarker, PolyLine, Polygon, Rectangle  # noqa

import branca
if tuple(int(x) for x in branca.__version__.split('.')) < (0, 3, 0):
    raise ImportError('branca version 0.3.0 or higher is required. '
                      'Update branca with e.g. `pip install branca --upgrade`.')

__version__ = get_versions()['version']
del get_versions

__all__ = [
    'CssLink',
    'Div',
    'Element',
    'Figure',
    'Html',
    'IFrame',
    'JavascriptLink',
    'Link',
    'MacroElement',
    'ColorMap',
    'ColorLine',
    'LinearColormap',
    'StepColormap',
    'Map',
    'FeatureGroup',
    'FitBounds',
    'Icon',
    'LayerControl',
    'Marker',
    'Popup',
    'Tooltip',
    'TileLayer',
    'ClickForMarker',
    'CustomIcon',
    'DivIcon',
    'GeoJson',
    'GeoJsonStyle',
    'LatLngPopup',
    'MarkerCluster',
    'Vega',
    'VegaLite',
    'RegularPolygonMarker',
    'TopoJson',
    'WmsTileLayer',
    # vector_layers
    'Circle',
    'CircleMarker',
    'PolyLine',
    'Polygon',
    'Polyline',
    'Rectangle',
]
