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

    m = folium.Map(location=(30, 20), zoom_start=4)
    minimap = plugins.MiniMap(tile_layer="Stamen Toner")
    minimap.add_to(m)

    out = normalize(m._parent.render())
    # verify that Stamen Toner tiles are being used
    assert "https://stamen-tiles" in out
