# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import sys
import warnings

import branca
from branca.colormap import (ColorMap, LinearColormap, StepColormap)
from branca.element import (
    CssLink,
    Div,
    Element,
    Figure,
    Html,
    IFrame,
    JavascriptLink,
    Link,
    MacroElement,
)

from folium._version import get_versions
from folium.features import (
    Choropleth,
    ClickForMarker,
    ColorLine,
    CustomIcon,
    DivIcon,
    GeoJson,
    GeoJsonTooltip,
    LatLngPopup,
    RegularPolygonMarker,
    TopoJson,
    Vega,
    VegaLite,
)
from folium.folium import Map
from folium.map import (
    FeatureGroup,
    FitBounds,
    Icon,
    LayerControl,
    Marker,
    Popup,
    Tooltip,
)
from folium.raster_layers import TileLayer, WmsTileLayer
from folium.vector_layers import Circle, CircleMarker, PolyLine, Polygon, Rectangle

if tuple(int(x) for x in branca.__version__.split('.')[:2]) < (0, 3):
    raise ImportError('branca version 0.3.0 or higher is required. '
                      'Update branca with e.g. `pip install branca --upgrade`.')

if sys.version_info < (3, 0):
    warnings.warn(
        ('This version of folium is the last to support Python 2.'
         ' Transition to Python 3 to be able to receive updates and fixes.'
         ' Check out https://python3statement.org/ for more info.'),
        UserWarning
    )

__version__ = get_versions()['version']
del get_versions

__all__ = [
    'Choropleth',
    'ClickForMarker',
    'ColorLine',
    'ColorMap',
    'CssLink',
    'CustomIcon',
    'Div',
    'DivIcon',
    'Element',
    'FeatureGroup',
    'Figure',
    'FitBounds',
    'GeoJson',
    'GeoJsonTooltip',
    'Html',
    'IFrame',
    'Icon',
    'JavascriptLink',
    'LatLngPopup',
    'LayerControl',
    'LinearColormap',
    'Link',
    'MacroElement',
    'Map',
    'Marker',
    'Popup',
    'RegularPolygonMarker',
    'StepColormap',
    'TileLayer',
    'Tooltip',
    'TopoJson',
    'Vega',
    'VegaLite',
    'WmsTileLayer',
    # vector_layers
    'Circle',
    'CircleMarker',
    'PolyLine',
    'Polygon',
    'Rectangle',
]
