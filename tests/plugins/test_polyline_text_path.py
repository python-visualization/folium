"""
Test PolyLineTextPath
---------------
"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_polyline_text_path():
    m = folium.Map([20.0, 0.0], zoom_start=3)

    wind_locations = [
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

    wind_line = folium.PolyLine(wind_locations, weight=15, color="#8EE9FF")
    attr = {"fill": "#007DEF", "font-weight": "bold", "font-size": "24"}
    wind_textpath = plugins.PolyLineTextPath(
        wind_line, ") ", repeat=True, offset=7, attributes=attr
    )

    m.add_child(wind_line)
    m.add_child(wind_textpath)

    out = normalize(m._parent.render())

    # We verify that the script import is present.
    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-textpath@1.2.3/leaflet.textpath.min.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template(
        """
        {{ this.polyline.get_name() }}.setText(
            "{{this.text}}",
            {{ this.options|tojavascript }}
        );
        """
    )

    expected = normalize(tmpl.render(this=wind_textpath))
    assert expected in out
