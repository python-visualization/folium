# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.colormap import (ColorMap, LinearColormap, StepColormap)
from branca.element import (CssLink, Div, Element, Figure, Html, IFrame,
                            JavascriptLink, Link, MacroElement)

from folium._version import get_versions

from folium.features import (
    Circle, CircleMarker, ClickForMarker, CustomIcon, DivIcon, GeoJson,
    LatLngPopup, PolyLine, RegularPolygonMarker, TopoJson, Vega, VegaLite,
    WmsTileLayer,
)

from folium.folium import Map

from folium.map import (
    FeatureGroup, FitBounds, Icon, LayerControl, Marker, Popup, TileLayer
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
    'LinearColormap',
    'StepColormap',
    'Map',
    'Circle',
    'CircleMarker',
    'RectangleMarker',
    'Polygon',
    'FeatureGroup',
    'FitBounds',
    'Icon',
    'LayerControl',
    'Marker',
    'Popup',
    'TileLayer',
    'ClickForMarker',
    'CustomIcon',
    'DivIcon',
    'GeoJson',
    'GeoJsonStyle',
    'LatLngPopup',
    'MarkerCluster',
    'PolyLine',
    'Vega',
    'VegaLite',
    'RegularPolygonMarker',
    'TopoJson',
    'WmsTileLayer'
]
