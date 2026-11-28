"""
Test Realtime
------------------
"""

import folium
from folium.plugins import MarkerCluster, Realtime
from folium.template import Template
from folium.utilities import JsCode, normalize


def test_realtime():
    m = folium.Map(location=[40.73, -73.94], zoom_start=12)
    source = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson"

    container = MarkerCluster().add_to(m)

    rt = Realtime(
        source,
        get_feature_id=JsCode("(f) => { return f.properties.objectid }"),
        point_to_layer=JsCode(
            "(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"
        ),
        container=container,
        interval=10000,
    )
    rt.add_to(m)

    tmpl_for_expected = Template("""
          {% macro script(this, kwargs) %}
              var {{ this.get_name() }}_options = {{ this.options|tojavascript }};
              {% for key, value in this.functions.items() %}
              {{ this.get_name() }}_options["{{key}}"] = {{ value }};
              {% endfor %}

              {% if this.container -%}
                  {{ this.get_name() }}_options["container"]
                      = {{ this.container.get_name() }};
              {% endif -%}

              var {{ this.get_name() }} = new L.realtime(
              {% if this.src is string or this.src is mapping -%}
                  {{ this.src|tojson }},
              {% else -%}
                  {{ this.src.js_code }},
              {% endif -%}
                  {{ this.get_name() }}_options
              );
              {{ this._parent.get_name() }}.addLayer(
                  {{ this.get_name() }}._container);
          {% endmacro %}
    """)
    expected = normalize(tmpl_for_expected.render(this=rt))

    out = normalize(m._parent.render())

    # We verify that imports
    assert (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-realtime/2.2.0/leaflet-realtime.js"></script>'  # noqa
        in out
    )  # noqa

    assert expected in out


def test_realtime_layer_options():
    m = folium.Map()
    source = "https://example.com/data.geojson"
    hidden = Realtime(source, name="Hidden", show=False).add_to(m)
    shown = Realtime(source, name="Shown").add_to(m)
    Realtime(source, name="Not in control", control=False).add_to(m)
    layer_control = folium.LayerControl().add_to(m)

    out = normalize(m._parent.render())

    assert hidden.layer_name == "Hidden"
    assert '"name"' not in out
    assert '"show"' not in out
    assert f"{hidden.get_name()}.addTo(" not in out
    assert f"{hidden.get_name()}._container" not in out
    assert out.count(f"{shown.get_name()}.addTo(") == 1
    assert list(layer_control.overlays) == ["Hidden", "Shown"]
