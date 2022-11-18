"""
Test pattern
---------------

"""

import os

import folium
from folium import plugins
from folium.utilities import normalize


def test_pattern():
    m = folium.Map([40.0, -105.0], zoom_start=6)

    stripes = plugins.pattern.StripePattern(angle=-45)
    stripes.add_to(m)
    circles = plugins.pattern.CirclePattern(
        width=20, height=20, radius=5, fill_opacity=0.5, opacity=1
    )

    def style_function(feature):
        default_style = {
            "opacity": 1.0,
            "fillColor": "#ffff00",
            "color": "black",
            "weight": 2,
        }

        if feature["properties"]["name"] == "Colorado":
            default_style["fillPattern"] = stripes
            default_style["fillOpacity"] = 1.0

        if feature["properties"]["name"] == "Utah":
            default_style["fillPattern"] = circles
            default_style["fillOpacity"] = 1.0

        return default_style

    data = os.path.join(os.path.dirname(__file__), os.pardir, "us-states.json")
    folium.GeoJson(data, style_function=style_function).add_to(m)

    out = normalize(m._parent.render())

    # We verify that the script import is present.
    script = '<script src="https://teastman.github.io/Leaflet.pattern/leaflet.pattern.js"></script>'  # noqa
    assert script in out
