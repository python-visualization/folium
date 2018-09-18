# -*- coding: utf-8 -*-

"""
Test BoatMarker
---------------

"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins


def test_pattern():
    m = folium.Map([40., -105.], zoom_start=6)

    remote_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    stripes = plugins.pattern.StripePattern(angle=-45)
    stripes.add_to(m)

    circles = plugins.pattern.CirclePattern(width=20, height=20, radius=5, fill_opacity=0.5, opacity=1)
    circles.add_to(m)

    def style_function(feature):
        default_style = {
            'opacity':1.0,
            'fillColor': '#ffff00',
            'color': 'black',
            'weight': 2
        }

        if feature['properties']['name'] == 'Colorado':
            default_style['fillPattern'] = stripes
            default_style['fillOpacity'] = 1.0

        if feature['properties']['name'] == 'Utah':
            default_style['fillPattern'] = circles
            default_style['fillOpacity'] = 1.0

        return default_style

    # Adding remote GeoJSON as additional layer.
    folium.GeoJson(remote_url, smooth_factor=0.5, style_function=style_function).add_to(m)

    out = m._parent.render()

    # We verify that the script import is present.
    script = '<script src="https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js"></script>'  # noqa
    assert script in out
