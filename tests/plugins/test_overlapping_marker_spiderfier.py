"""
Test OverlappingMarkerSpiderfier
--------------------------------
"""

import numpy as np

from folium.folium import Map
from folium.map import Marker
from folium.plugins.overlapping_marker_spiderfier import OverlappingMarkerSpiderfier


def test_oms_js_inclusion():
    """
    Test that the OverlappingMarkerSpiderfier JavaScript library is included in the map.
    """
    m = Map([45.05, 3.05], zoom_start=14)
    OverlappingMarkerSpiderfier().add_to(m)

    rendered_map = m._parent.render()
    assert (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/OverlappingMarkerSpiderfier-Leaflet/0.2.6/oms.min.js"></script>'
        in rendered_map
    ), "OverlappingMarkerSpiderfier JS file is missing in the rendered output."


def test_marker_addition():
    """
    Test that markers are correctly added to the map.
    """
    N = 10
    np.random.seed(seed=26082009)
    data = np.array(
        [
            np.random.uniform(low=45.0, high=45.1, size=N),
            np.random.uniform(low=3.0, high=3.1, size=N),
        ]
    ).T

    m = Map([45.05, 3.05], zoom_start=14)
    markers = [
        Marker(
            location=loc,
            popup=f"Marker {i}",
        )
        for i, loc in enumerate(data)
    ]

    for marker in markers:
        marker.add_to(m)

    assert (
        len(m._children) == len(markers) + 1
    ), f"Expected {len(markers)} markers, found {len(m._children) - 1}."


def test_map_bounds():
    """
    Test that the map bounds correctly encompass all added markers.
    """
    N = 10
    np.random.seed(seed=26082009)
    data = np.array(
        [
            np.random.uniform(low=45.0, high=45.1, size=N),
            np.random.uniform(low=3.0, high=3.1, size=N),
        ]
    ).T

    m = Map([45.05, 3.05], zoom_start=14)
    markers = [
        Marker(
            location=loc,
            popup=f"Marker {i}",
        )
        for i, loc in enumerate(data)
    ]

    for marker in markers:
        marker.add_to(m)

    bounds = m.get_bounds()
    assert bounds is not None, "Map bounds should not be None"

    min_lat, min_lon = data.min(axis=0)
    max_lat, max_lon = data.max(axis=0)

    assert (
        bounds[0][0] <= min_lat
    ), "Map bounds do not correctly include the minimum latitude."
    assert (
        bounds[0][1] <= min_lon
    ), "Map bounds do not correctly include the minimum longitude."
    assert (
        bounds[1][0] >= max_lat
    ), "Map bounds do not correctly include the maximum latitude."
    assert (
        bounds[1][1] >= max_lon
    ), "Map bounds do not correctly include the maximum longitude."


def test_overlapping_marker_spiderfier_integration():
    """
    Test that OverlappingMarkerSpiderfier integrates correctly with the map.
    """
    m = Map([45.05, 3.05], zoom_start=14)
    oms = OverlappingMarkerSpiderfier(
        keep_spiderfied=True,
        nearby_distance=20,
    )
    oms.add_to(m)

    assert (
        oms.get_name() in m._children
    ), "OverlappingMarkerSpiderfier is not correctly added to the map."
