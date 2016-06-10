# -*- coding: utf-8 -*-
"""
Test BoatMarker
---------------

"""
from jinja2 import Template

import folium
from folium import plugins


def test_boat_marker():
    m = folium.Map([30., 0.], zoom_start=3)
    bm1 = plugins.BoatMarker(
        (34, -43),
        heading=45,
        wind_heading=150,
        wind_speed=45,
        color="#8f8")
    bm2 = plugins.BoatMarker(
        (46, -30),
        heading=-20,
        wind_heading=46,
        wind_speed=25,
        color="#88f")

    m.add_child(bm1)
    m.add_child(bm2)
    m._repr_html_()

    out = m._parent.render()

    # We verify that the script import is present.
    script = '<script src="https://thomasbrueggemann.github.io/leaflet.boatmarker/js/leaflet.boatmarker.min.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template("""
                var {{this.get_name()}} = L.boatMarker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                {{this.get_name()}}.setHeadingWind({{this.heading}}, {{this.wind_speed}}, {{this.wind_heading}});
    """)  # noqa

    assert tmpl.render(this=bm1) in out
    assert tmpl.render(this=bm2) in out

    bounds = m.get_bounds()
    assert bounds == [[34, -43], [46, -30]], bounds
