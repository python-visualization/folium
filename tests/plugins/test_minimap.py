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
