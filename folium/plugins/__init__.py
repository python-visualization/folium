"""Wrap some of the most popular leaflet external plugins."""

from folium.plugins.antpath import AntPath
from folium.plugins.beautify_icon import BeautifyIcon
from folium.plugins.boat_marker import BoatMarker
from folium.plugins.draw import Draw
from folium.plugins.dual_map import DualMap
from folium.plugins.encoded import PolygonFromEncoded, PolyLineFromEncoded
from folium.plugins.fast_marker_cluster import FastMarkerCluster
from folium.plugins.feature_group_sub_group import FeatureGroupSubGroup
from folium.plugins.float_image import FloatImage
from folium.plugins.fullscreen import Fullscreen
from folium.plugins.geocoder import Geocoder
from folium.plugins.groupedlayercontrol import GroupedLayerControl
from folium.plugins.heat_map import HeatMap
from folium.plugins.heat_map_withtime import HeatMapWithTime
from folium.plugins.locate_control import LocateControl
from folium.plugins.marker_cluster import MarkerCluster
from folium.plugins.measure_control import MeasureControl
from folium.plugins.minimap import MiniMap
from folium.plugins.mouse_position import MousePosition
from folium.plugins.overlapping_marker_spiderfier import OverlappingMarkerSpiderfier
from folium.plugins.pattern import CirclePattern, StripePattern
from folium.plugins.polyline_offset import PolyLineOffset
from folium.plugins.polyline_text_path import PolyLineTextPath
from folium.plugins.realtime import Realtime
from folium.plugins.scroll_zoom_toggler import ScrollZoomToggler
from folium.plugins.search import Search
from folium.plugins.semicircle import SemiCircle
from folium.plugins.side_by_side import SideBySideLayers
from folium.plugins.tag_filter_button import TagFilterButton
from folium.plugins.terminator import Terminator
from folium.plugins.time_slider_choropleth import TimeSliderChoropleth
from folium.plugins.timeline import Timeline, TimelineSlider
from folium.plugins.timestamped_geo_json import TimestampedGeoJson
from folium.plugins.timestamped_wmstilelayer import TimestampedWmsTileLayers
from folium.plugins.treelayercontrol import TreeLayerControl
from folium.plugins.vectorgrid_protobuf import VectorGridProtobuf

__all__ = [
    "AntPath",
    "BeautifyIcon",
    "BoatMarker",
    "CirclePattern",
    "Draw",
    "DualMap",
    "FastMarkerCluster",
    "FeatureGroupSubGroup",
    "FloatImage",
    "Fullscreen",
    "Geocoder",
    "GroupedLayerControl",
    "HeatMap",
    "HeatMapWithTime",
    "LocateControl",
    "MarkerCluster",
    "MeasureControl",
    "MiniMap",
    "MousePosition",
    "OverlappingMarkerSpiderfier",
    "PolygonFromEncoded",
    "PolyLineFromEncoded",
    "PolyLineTextPath",
    "PolyLineOffset",
    "Realtime",
    "ScrollZoomToggler",
    "Search",
    "SemiCircle",
    "SideBySideLayers",
    "StripePattern",
    "TagFilterButton",
    "Terminator",
    "TimeSliderChoropleth",
    "Timeline",
    "TimelineSlider",
    "TimestampedGeoJson",
    "TimestampedWmsTileLayers",
    "TreeLayerControl",
    "VectorGridProtobuf",
]
