# -*- coding: utf-8 -*-
"""
Test Fullscreen
-----------------------
"""
import folium
from folium import plugins


def test_fullscreen():
    m = folium.Map([47, 3], zoom_start=1)
    fs = plugins.Fullscreen()
    m.add_child(fs)
    m._repr_html_()

    out = m._parent.render()

    # verify that the fullscreen control was rendered
    assert 'L.control.fullscreen().addTo' in out
