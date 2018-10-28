# -*- coding: utf-8 -*-

"""
Test MiniMap
---------------
"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins


def test_minimap():
    m = folium.Map(location=(30, 20), zoom_start=4)

    minimap = plugins.MiniMap()
    m.add_child(minimap)

    out = m._parent.render()

    # Verify that a new minimap is getting created.
    assert 'new L.Control.MiniMap' in out

    m = folium.Map(location=(30, 20), zoom_start=4)
    minimap = plugins.MiniMap(tile_layer="Stamen Toner")
    minimap.add_to(m)

    out = m._parent.render()
    # verify that Stamen Toner tiles are being used
    assert 'https://stamen-tiles' in out
