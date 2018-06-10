# -*- coding: utf-8 -*-

"""
Test MarkerCluster
------------------
"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins

from jinja2 import Template


def test_feature_group_sub_group():
    m = folium.Map([0., 0.], zoom_start=6)
    fg = folium.FeatureGroup()
    m.add_child(fg)
    g1 = plugins.FeatureGroupSubGroup(fg, 'g1')
    m.add_child(g1)
    folium.Marker([1, 1]).add_to(g1)
    folium.Marker([-1, -1]).add_to(g1)
    g2 = plugins.FeatureGroupSubGroup(fg, 'g2')
    folium.Marker([-1, 1]).add_to(g2)
    folium.Marker([1, -1]).add_to(g2)
    m.add_child(g2)
    folium.LayerControl().add_to(m)
    m._repr_html_()

    out = m._parent.render()

    # We verify that imports
    assert '<script src="https://unpkg.com/leaflet.featuregroup.subgroup@1.0.2/dist/leaflet.featuregroup.subgroup.js"></script>' in out  # noqa

    # Verify the script part is okay.
    tmpl = Template("""
        var {{this.get_name()}} = L.featureGroup.subGroup({{this._group.get_name()}});
        {{this.get_name()}}.addTo({{this._parent.get_name()}});
    """)
    assert ''.join(tmpl.render(this=g1).split()) in ''.join(out.split())
    assert ''.join(tmpl.render(this=g2).split()) in ''.join(out.split())
