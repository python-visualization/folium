# -*- coding: utf-8 -*-

import sys

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

from folium.features import (
    Choropleth,
    ClickForMarker,
    ColorLine,
    CustomIcon,
    DivIcon,
    GeoJson,
    GeoJsonTooltip,
    GeoJsonPopup,
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

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"


if tuple(int(x) for x in branca.__version__.split('.')[:2]) < (0, 3):
    raise ImportError('branca version 0.3.0 or higher is required. '
                      'Update branca with e.g. `pip install branca --upgrade`.')

if sys.version_info < (3, 0):
    raise ImportError(
        """You are running folium {} on Python 2
    
    folium 0.9 and above are no longer compatible with Python 2, but somehow
    you got this version anyway. Make sure you have pip >= 9.0 to avoid this
    kind of issue, as well as setuptools >= 24.2:
    
     $ pip install pip setuptools --upgrade
    
    Your choices:
    
    - Upgrade to Python 3.
    
    - Install an older version of folium:
    
     $ pip install 'folium<0.9.0'
    
    """.format(__version__))  # noqa

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
