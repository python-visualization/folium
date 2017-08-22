# -*- coding: utf-8 -*-
"""
Folium plugins
--------------

Add different objects/effects on a folium map.
"""

from .boat_marker import BoatMarker
from .fast_marker_cluster import FastMarkerCluster
from .float_image import FloatImage
from .fullscreen import Fullscreen
from .heat_map import HeatMap
from .image_overlay import ImageOverlay
from .marker_cluster import MarkerCluster
from .polyline_text_path import PolyLineTextPath
from .scroll_zoom_toggler import ScrollZoomToggler
from .terminator import Terminator
from .timestamped_geo_json import TimestampedGeoJson
from .timestamped_wmstilelayer import TimestampedWmsTileLayers

__all__ = [
    'MarkerCluster',
    'FastMarkerCluster',
    'ScrollZoomToggler',
    'Terminator',
    'BoatMarker',
    'TimestampedGeoJson',
    'HeatMap',
    'ImageOverlay',
    'Fullscreen',
    'PolyLineTextPath',
    'FloatImage',
    'TimestampedWmsTileLayers'
    ]
