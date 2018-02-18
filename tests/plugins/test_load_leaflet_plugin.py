# -*- coding: utf-8 -*-


from __future__ import (absolute_import, division, print_function)

import re

import folium
from folium import plugins

ROTATE_MARKER_URL = 'https://cdn.rawgit.com/bbecquet/Leaflet.RotatedMarker/master/leaflet.rotatedMarker.js'
DUMMY_PLUGIN = 'https://dummy.plugin/something.js'


def test_load_leaflet_plugin():
    m = folium.Map([30., 0.], zoom_start=3)
    loader = plugins.LoadLeafletPlugin(ROTATE_MARKER_URL)
    m.add_child(loader)

    out = m._parent.render()

    assert '<script src="{}"></script>'.format(ROTATE_MARKER_URL) in out


def test_loads_multiple_plugins():
    m = folium.Map([30., 0.], zoom_start=3)
    loader = plugins.LoadLeafletPlugin(ROTATE_MARKER_URL, DUMMY_PLUGIN)
    m.add_child(loader)

    out = m._parent.render()

    assert '<script src="{}"></script>'.format(ROTATE_MARKER_URL) in out
    assert '<script src="{}"></script>'.format(DUMMY_PLUGIN) in out


def test_doesnt_load_leaflet_plugin_multiple_times():
    """
    I noticed that when running in Jupyter we would add the same <script>-tag
    multiple times, and I don't know why. By making this test pass I managed to
    get the Jupyter notebook to only render it once (and get the expected result
    using rotate marker URL).
    """
    m = folium.Map([30., 0.], zoom_start=3)
    loader = plugins.LoadLeafletPlugin(ROTATE_MARKER_URL, ROTATE_MARKER_URL)
    m.add_child(loader)

    out = m._parent.render()

    matches = re.findall(r'<script src="{}"></script>'.format(ROTATE_MARKER_URL), out)
    assert 1 == len(matches), 'expected to find plugin loaded only once'
