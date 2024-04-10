"""Test PolyLineFromEncoded Plugin."""

from folium import Map
from folium.plugins import PolyLineFromEncoded
from folium.utilities import normalize


def test_polyline_from_encoded():
    """Test `PolyLineFromEncoded` plugin.

    The test ensures:
        - The original JS script is present in the HTML file.
        - The rendering from `PolyLineFromEncoded` and the original plugin gives the
            same output.
    """

    m = Map([35.0, -120.0], zoom_start=3)

    encoded = r"_p~iF~cn~U_ulLn{vA_mqNvxq`@"
    kwargs = {"color": "green"}
    polyline = PolyLineFromEncoded(encoded=encoded, **kwargs)

    polyline.add_to(m)

    out = normalize(m._parent.render())

    script = '<script src="https://cdn.jsdelivr.net/npm/polyline-encoded@0.0.9/Polyline.encoded.js"></script>'
    assert script in out

    expected_render = f"""
    var {polyline.get_name()} = L.Polyline.fromEncoded(
        "{encoded}", {{"color": "green"}}
    ).addTo({m.get_name()});
    """

    actual_render = polyline._template.module.script(polyline)

    assert normalize(expected_render) == normalize(actual_render)
