# -*- coding: utf-8 -*-
"""
Folium plugins
--------------

Add different objects/effects on a folium map.
"""

from .marker_cluster import MarkerCluster
from .scroll_zoom_toggler import ScrollZoomToggler
from .terminator import Terminator
from .boat_marker import BoatMarker
from .timestamped_geo_json import TimestampedGeoJson
from .heat_map import HeatMap
from .image_overlay import ImageOverlay
from .fullscreen import Fullscreen
from .polyline_text_path import PolyLineTextPath
from .float_image import FloatImage

__all__ = [
    'MarkerCluster',
    'ScrollZoomToggler',
    'Terminator',
    'BoatMarker',
    'TimestampedGeoJson',
    'HeatMap',
    'ImageOverlay',
    'Fullscreen',
    'PolyLineTextPath',
    'FloatImage'
    ]
