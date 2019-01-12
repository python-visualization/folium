# -*- coding: utf-8 -*-

"""
Test DualMap
------------
"""

from __future__ import (absolute_import, division, print_function)

from jinja2 import Template

import folium
import folium.plugins


def test_dual_map():
    m = folium.plugins.DualMap((0, 0))

    folium.FeatureGroup(name='both').add_to(m)
    folium.FeatureGroup(name='left').add_to(m.m1)
    folium.FeatureGroup(name='right').add_to(m.m2)

    figure = m.get_root()
    assert isinstance(figure, folium.Figure)
    out = figure.render()

    script = '<script src="https://rawcdn.githack.com/jieter/Leaflet.Sync/master/L.Map.Sync.js"></script>'  # noqa
    assert script in out

    tmpl = Template("""
        {{ this.m1.get_name() }}.sync({{ this.m2.get_name() }});
        {{ this.m2.get_name() }}.sync({{ this.m1.get_name() }});
    """)

    assert tmpl.render(this=m) in out
