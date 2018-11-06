# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import sys
import warnings

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
if tuple(int(x) for x in branca.__version__.split('.')[:2]) < (0, 3):
    raise ImportError('branca version 0.3.0 or higher is required. '
                      'Update branca with e.g. `pip install branca --upgrade`.')

if sys.version_info < (3, 0):
    warnings.warn(
        ("folium will stop working with Python 2.7 starting Jan. 1, 2019."
         " Please transition to Python 3 before this time."
         " Check out https://python3statement.org/ for more info."),
        PendingDeprecationWarning
    )

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
