"""Test PolyLineFromEncoded Plugin."""

from jinja2 import Template

from folium import Map
from folium.plugins import PolygonFromEncoded, PolyLineFromEncoded
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

    tmpl = Template(
        """
        var {{this.get_name()}} = L.Polyline.fromEncoded(
                        {{ this.encoded|tojson }},
                        {{ this.options|tojson }}
        ).addTo({{this._parent.get_name()}});
        """
    )

    expected_render = tmpl.render(this=polyline)
    actual_render = polyline._template.module.script(polyline)

    assert normalize(expected_render) == normalize(actual_render)


def test_polygon_from_encoded():
    """Test `PolygonFromEncoded` plugin.

    The test ensures:
        - The original JS script is present in the HTML file.
        - The rendering from `PolygonFromEncoded` and the original plugin gives the
            same output.
    """

    m = Map([40.0, -80.0], zoom_start=3)

    encoded = r"w`j~FpxivO}jz@qnnCd}~Bsa{@~f`C`lkH"
    polygon = PolygonFromEncoded(encoded=encoded, kwargs={})

    polygon.add_to(m)

    out = normalize(m._parent.render())

    script = '<script src="https://cdn.jsdelivr.net/npm/polyline-encoded@0.0.9/Polyline.encoded.js"></script>'
    assert script in out

    tmpl = Template(
        """
        var {{this.get_name()}} = L.Polygon.fromEncoded(
                            {{ this.encoded|tojson }},
                            {{ this.options|tojson }}
        )
        .addTo({{this._parent.get_name()}});
        """
    )

    expected_render = tmpl.render(this=polygon)

    actual_render = polygon._template.module.script(polygon)

    assert normalize(expected_render) == normalize(actual_render)
