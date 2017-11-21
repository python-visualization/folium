# -*- coding: utf-8 -*-

"""
Test BoatMarker
---------------

"""

from __future__ import absolute_import, division, print_function

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
        color='#8f8')
    bm2 = plugins.BoatMarker(
        (46, -30),
        heading=-20,
        wind_heading=46,
        wind_speed=25,
        color='#88f')

    m.add_child(bm1)
    m.add_child(bm2)
    m._repr_html_()

    out = m._parent.render()

    # We verify that the script import is present.
    turfjs_script = '<script src="https://api.tiles.mapbox.com/mapbox.js/plugins/turf/v2.0.0/turf.min.js"></script>'  # noqa
    assert turfjs_script in out

    boatmarker_script = '<script src="https://unpkg.com/leaflet.boatmarker/leaflet.boatmarker.min.js"></script>'  # noqa
    assert boatmarker_script in out

    # We verify that the script part is correct.
    tmpl = Template("""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.boatMarker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                var animate = {{this.animate}}
                var boatMarker = {{this.get_name()}};
                boatMarker.setHeadingWind({{this.heading}},
                    {{this.wind_speed}}, {{this.wind_heading}});

                if (animate === 1) {
                    window.setInterval(function() {
                        var destination = turf.destination(
                            boatMarker.toGeoJSON(), 0.02, 60,"kilometers");

                        boatMarker.setLatLng(
                            destination.geometry.coordinates.reverse());
                    }, 488);
                }
            {% endmacro %}
    """)  # noqa

    assert tmpl.render(this=bm1) in out
    assert tmpl.render(this=bm2) in out

    bounds = m.get_bounds()
    assert bounds == [[34, -43], [46, -30]], bounds
