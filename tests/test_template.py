import folium
from folium.template import tojavascript
from folium.utilities import JsCode


def test_tojavascript():
    trail_coordinates = [
        (-71.351871840295871, -73.655963711222626),
        (-71.374144382613707, -73.719861619751498),
        (-71.391042575973145, -73.784922248007007),
        (-71.400964450973134, -73.851042243124397),
        (-71.402411391077322, -74.050048183880477),
    ]

    trail = folium.PolyLine(trail_coordinates, tooltip="Coast")
    d = {
        "label": "Base Layers",
        "children": [
            {
                "label": "World &#x1f5fa;",
                "children": [
                    {"label": "trail", "layer": trail},
                    {"jscode": JsCode('function(){return "hi"}')},
                ],
            }
        ],
    }
    js = tojavascript(d)
    assert "poly_line" in js
    assert 'return "hi"' in js
