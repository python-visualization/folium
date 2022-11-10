"""
Test SemiCircle
---------------

"""

import folium
from folium import plugins
from folium.utilities import normalize

from jinja2 import Template


def test_semicircle():
    m = folium.Map([30., 0.], zoom_start=3)
    sc1 = plugins.SemiCircle(
        (34, -43),
        radius=400000,
        arc=300,
        direction=20,
        color='red',
        fill_color='red',
        opacity=0,
        popup='Direction - 20 degrees, arc 300 degrees'
    )
    sc2 = plugins.SemiCircle(
        (46, -30),
        radius=400000,
        start_angle=10,
        stop_angle=50,
        color='red',
        fill_color='red',
        opacity=0,
        popup='Start angle - 10 degrees, Stop angle - 50 degrees'
    )

    m.add_child(sc1)
    m.add_child(sc2)
    m._repr_html_()

    out = normalize(m._parent.render())

    # We verify that the script import is present.
    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-semicircle@2.0.4/Semicircle.min.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl_sc1 = Template(u"""
        var {{ this.get_name() }} = L.semiCircle(
        {{ this.location|tojson }},
        {{ this.options | tojson }}
        )
            .setDirection{{ this.direction }}
        .addTo({{ this._parent.get_name() }});
    """)

    tmpl_sc2 = Template(u"""
        var {{ this.get_name() }} = L.semiCircle(
        {{ this.location|tojson }},
        {{ this.options | tojson }}
        )
        .addTo({{ this._parent.get_name() }});
    """)
    assert normalize(tmpl_sc1.render(this=sc1)) in out
    assert normalize(tmpl_sc2.render(this=sc2)) in out

    bounds = m.get_bounds()
    assert bounds == [[34, -43], [46, -30]], bounds
