"""
Test MiniMap
---------------
"""

import folium
from folium import plugins
from folium.utilities import normalize


def test_minimap():
    m = folium.Map(location=(30, 20), zoom_start=4)

    minimap = plugins.MiniMap()
    m.add_child(minimap)

    out = normalize(m._parent.render())

    # Verify that a new minimap is getting created.
    assert "new L.Control.MiniMap" in out

    m = folium.Map(tiles=None, location=(30, 20), zoom_start=4)
    minimap = plugins.MiniMap()
    minimap.add_to(m)

    out = normalize(m._parent.render())
    # verify that tiles are being used
    assert r"https://tile.openstreetmap.org" in out


def test_minimap_tile_layer_options_are_camelized():
    """The minimap's tile layer must get the same options as a regular one.

    Leaflet ignores snake_case keys such as ``tile_size``, so options like
    tileSize, zoomOffset and maxNativeZoom were lost on the minimap.
    """
    m = folium.Map(tiles=None)
    tile_layer = folium.TileLayer(
        "https://example.com/{z}/{x}/{y}.png",
        attr="example",
        tile_size=512,
        zoom_offset=-1,
        max_native_zoom=14,
    )
    plugins.MiniMap(tile_layer=tile_layer).add_to(m)

    out = normalize(m._parent.render())

    assert '"tileSize": 512' in out
    assert '"zoomOffset": -1' in out
    assert '"maxNativeZoom": 14' in out
    assert "tile_size" not in out
    assert "max_native_zoom" not in out
