"""
Test PolyLineDecorator
----------------------
"""

import pytest

import folium
from folium import plugins
from folium.utilities import normalize


def test_polyline_decorator():
    m = folium.Map([46.5, 6.6], zoom_start=9)
    line = folium.PolyLine([[46.2, 6.15], [46.52, 6.63]]).add_to(m)
    decorator = plugins.PolyLineDecorator(
        line,
        [
            {
                "offset": "100%",
                "repeat": 0,
                "symbol": {"type": "arrowHead", "pixel_size": 15},
            }
        ],
    ).add_to(m)

    out = normalize(m._parent.render())

    script = '<script src="https://cdn.jsdelivr.net/npm/leaflet-polylinedecorator@1.6.0/dist/leaflet.polylineDecorator.min.js"></script>'  # noqa
    assert script in out
    expected = normalize(f"""
        var {decorator.get_name()} = L.polylineDecorator(
            {line.get_name()},
            {{
                "patterns": [
                    {{
                        "offset": "100%",
                        "repeat": 0,
                        "symbol": L.Symbol.arrowHead({{
                            "pixelSize": 15,
                        }}),
                    }},
                ],
            }}
        ).addTo({m.get_name()});
        """)
    assert expected in out


def test_polyline_decorator_unknown_symbol():
    line = folium.PolyLine([[0, 0], [1, 1]])
    with pytest.raises(ValueError):
        plugins.PolyLineDecorator(line, [{"symbol": {"type": "arrow"}}])
