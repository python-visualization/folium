# -*- coding: utf-8 -*-
'''
Folium Features Tests
---------------------

'''
import folium
from folium import features
import numpy as np
import json

class testFeatures(object):
    '''Test class for Folium features'''

    def test_map_creation(self):
        mapa = features.Map([45.,3.], zoom_start=4)
        mapa.add_plugin(plugins.ScrollZoomToggler())
        mapa._build_map()
