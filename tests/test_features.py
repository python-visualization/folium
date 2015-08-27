# -*- coding: utf-8 -*-
'''
Folium Features Tests
---------------------

'''
from folium import features
from folium.six import text_type, binary_type
import numpy as np
import json

class testFeatures(object):
    '''Test class for Folium features'''

    def test_map_creation(self):
        m = features.Map([40,-100], zoom_start=4)

    def test_figure_creation(self):
        f = features.Figure()

    def test_figure_rendering(self):
        f = features.Figure()
        out = f.render()
        assert type(out) is text_type

    def test_figure_double_rendering(self):
        f = features.Figure()
        out = f.render()
        out2 = f.render()
        assert out==out2

    def test_wms_service(self):
        m = features.Map([40,-100], zoom_start=4)
        w = features.WmsTileLayer("http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
                name='test',
                format='image/png',
                layers='nexrad-n0r-900913',
                attribution=u"Weather data © 2012 IEM Nexrad",
                transparent=True)
        w.add_to(m)
        m._repr_html_()
