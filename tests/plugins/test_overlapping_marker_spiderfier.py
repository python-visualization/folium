"""
Test OverlappingMarkerSpiderfier
--------------------------------
"""

import numpy as np

from folium.folium import Map
from folium.map import FeatureGroup, Marker
from folium.plugins.overlapping_marker_spiderfier import OverlappingMarkerSpiderfier
from folium.utilities import normalize


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


def test_markers_found_when_added_with_add_child():
    m = Map([45.05, 3.05], zoom_start=14)
    markers = [Marker([45.05, 3.05]).add_to(m) for _ in range(3)]
    oms = OverlappingMarkerSpiderfier()
    m.add_child(oms)

    out = normalize(m.get_root().render())

    for marker in markers:
        assert f"oms.addMarker({marker.get_name()});" in out


def test_markers_added_to_group_after_plugin_are_found():
    m = Map([45.05, 3.05], zoom_start=14)
    group = FeatureGroup().add_to(m)
    OverlappingMarkerSpiderfier().add_to(m)
    marker = Marker([45.05, 3.05]).add_to(group)

    out = normalize(m.get_root().render())

    assert f"oms.addMarker({marker.get_name()});" in out


def test_added_to_feature_group_uses_the_map():
    m = Map([45.05, 3.05], zoom_start=14)
    group = FeatureGroup().add_to(m)
    inside = [Marker([45.05, 3.05]).add_to(group) for _ in range(2)]
    outside = Marker([45.05, 3.05]).add_to(m)
    OverlappingMarkerSpiderfier().add_to(group)

    out = normalize(m.get_root().render())

    assert f"new OverlappingMarkerSpiderfier({m.get_name()}," in out
    assert f"{m.get_name()}.closePopup();" in out
    assert f"new OverlappingMarkerSpiderfier({group.get_name()}," not in out
    for marker in inside:
        assert f"oms.addMarker({marker.get_name()});" in out
    assert f"oms.addMarker({outside.get_name()});" not in out
