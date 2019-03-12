# -*- coding: utf-8 -*-

"""
Test PolyLineOffset
-------------------
"""

from __future__ import absolute_import, division, print_function

import folium
from folium import plugins

from jinja2 import Template

import pytest


@pytest.mark.parametrize("offset", [0, 10, -10])
def test_polylineoffset(offset):
    m = folium.Map([20.0, 0.0], zoom_start=3)

    locations = [
        [59.355600, -31.99219],
        [55.178870, -42.89062],
        [47.754100, -43.94531],
        [38.272690, -37.96875],
        [27.059130, -41.13281],
        [16.299050, -36.56250],
        [8.4071700, -30.23437],
        [1.0546300, -22.50000],
        [-8.754790, -18.28125],
        [-21.61658, -20.03906],
        [-31.35364, -24.25781],
        [-39.90974, -30.93750],
        [-43.83453, -41.13281],
        [-47.75410, -49.92187],
        [-50.95843, -54.14062],
        [-55.97380, -56.60156],
    ]

    polylineoffset = plugins.PolyLineOffset(locations=locations, offset=offset)
    polylineoffset.add_to(m)

    m._repr_html_()
    out = m._parent.render()

    # We verify that the script import is present.
    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-polylineoffset@1.1.1/leaflet.polylineoffset.min.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template(
        """
                var {{this.get_name()}} = L.polyline(
                    {{this.location}},
                    {{ this.options }}
                    )
                    .addTo({{this._parent.get_name()}});
            """
    )  # noqa

    expected_rendered = tmpl.render(this=polylineoffset)
    rendered = polylineoffset._template.module.script(polylineoffset)
    assert folium.utilities.compare_rendered(expected_rendered, rendered)
