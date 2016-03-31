# -*- coding: utf-8 -*-

from __future__ import absolute_import

from folium.folium import Map, initialize_notebook, CircleMarker

from folium.map import (FeatureGroup, FitBounds, Icon, LayerControl, Marker,
                        Popup, TileLayer)

from folium.features import (ClickForMarker, CustomIcon, DivIcon,
                             GeoJson, LatLngPopup,
                             MarkerCluster, MultiPolyLine, PolyLine, Vega,
                             RegularPolygonMarker, TopoJson, WmsTileLayer)

import folium.colormap as colormap

__version__ = '0.2.1'

__all__ = ['Map',
           'initialize_notebook',
           'CircleMarker',
           'FeatureGroup',
           'FitBounds',
           'Icon',
           'LayerControl',
           'Marker',
           'Popup',
           'TileLayer',
           'ClickForMarker',
           'colormap',
           'CustomIcon',
           'DivIcon',
           'GeoJson',
           'GeoJsonStyle',
           'LatLngPopup',
           'MarkerCluster',
           'MultiPolyLine',
           'PolyLine',
           'Vega',
           'RegularPolygonMarker',
           'TopoJson',
           'WmsTileLayer']
