"""
Test LocateControl
------------------

"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import JsCode, normalize


def test_locate_control():
    m = folium.Map([47, 3], zoom_start=1)
    lc = plugins.LocateControl().add_to(m)

    out = normalize(m._parent.render())

    tmpl = Template("""
        var {{this.get_name()}} = L.control.locate(
            {{this.options | tojavascript}}
        ).addTo({{this._parent.get_name()}});
    """)
    assert normalize(tmpl.render(this=lc)) in out
    assert f"{lc.get_name()}.start();" not in out


def test_locate_control_auto_start():
    m = folium.Map()
    lc = plugins.LocateControl(auto_start=True).add_to(m)

    out = normalize(m._parent.render())

    assert f"{lc.get_name()}.start();" in out


def test_locate_control_snake_case_options():
    m = folium.Map()
    plugins.LocateControl(
        fly_to=True,
        keep_current_zoom_level=True,
        locate_options={"enable_high_accuracy": True},
    ).add_to(m)

    out = normalize(m._parent.render())

    assert '"flyTo": true' in out
    assert '"keepCurrentZoomLevel": true' in out
    assert '"enableHighAccuracy": true' in out
    assert "fly_to" not in out
    assert "keep_current_zoom_level" not in out


def test_locate_control_camel_case_options_unchanged():
    m = folium.Map()
    plugins.LocateControl(
        flyTo=True,
        strings={"title": "Show me where I am", "popup": "You are here"},
    ).add_to(m)

    out = normalize(m._parent.render())

    assert '"flyTo": true' in out
    assert '"title": "Show me where I am"' in out
    assert '"popup": "You are here"' in out


def test_locate_control_js_code_option():
    m = folium.Map()
    plugins.LocateControl(
        on_location_error=JsCode("function(err) { console.log(err.message); }"),
    ).add_to(m)

    out = normalize(m._parent.render())

    assert '"onLocationError": function(err) { console.log(err.message); }' in out
