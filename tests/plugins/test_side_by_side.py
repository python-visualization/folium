# -*- coding: utf-8 -*-

"""
Test MiniMap
---------------
"""

from __future__ import (absolute_import, division, print_function)

from folium import Map, TileLayer, WmsTileLayer, Marker
from folium.plugins import SideBySide
import pytest

def test_side_by_side():
    m = Map(location=[40, -100], zoom_start=4)
    url = 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    tile = TileLayer(tiles=url, attr='google', name='google street view',
                     max_zoom=20, subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                     overlay=False, control=True).add_to(m)
    url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
    wms = WmsTileLayer(url=url, name='test', fmt='image/png',
                       layers='nexrad-n0r-900913', 
                       attr=u'Weather data © 2012 IEM Nexrad', 
                       transparent=True, overlay=True, control=True).add_to(m)
    sbs = SideBySide(tile, wms)
    m.add_child(sbs)
    out = m._parent.render()
    # Verify that a new side-by-side control is getting created.
    assert 'new L.Control.SideBySide' in out
    
    m = Map(location=[40, -100], zoom_start=4)
    url = 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    tile = TileLayer(tiles=url, attr='google', name='google street view',
                     max_zoom=20, subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                     overlay=False, control=True).add_to(m)
    url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
    marker = Marker((40, -100))
    with pytest.raises(TypeError):
        sbs = SideBySide(tile, marker)
        sbs = SideBySide(marker, tile)
    
    m = Map(location=[40, -100], zoom_start=4)
    url = 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    tile = TileLayer(tiles=url, attr='google', name='google street view',
                     max_zoom=20, subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                     overlay=False, control=True).add_to(m)
    url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
    wms = WmsTileLayer(url=url, name='test', fmt='image/png',
                       layers='nexrad-n0r-900913', 
                       attr=u'Weather data © 2012 IEM Nexrad', 
                       transparent=True, overlay=True, control=True).add_to(m)
    with pytest.raises(ValueError):
        sbs = SideBySide(tile, wms, version="whatever")
    