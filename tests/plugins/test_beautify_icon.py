"""
Test BeautifyIcon
---------------

"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_beautify_icon():
    m = folium.Map([30.0, 0.0], zoom_start=3)
    # BeautifyIcons
    ic1 = plugins.BeautifyIcon(
        icon="plane", border_color="#b3334f", text_color="#b3334f"
    )
    ic2 = plugins.BeautifyIcon(
        border_color="#00ABDC",
        text_color="#00ABDC",
        number=10,
        inner_icon_style="margin-top:0;",
    )

    # Markers, add icons as keyword argument
    bm1 = folium.Marker(location=[46, -122], popup="Portland, OR", icon=ic1).add_to(m)

    bm2 = folium.Marker(location=[50, -121], icon=ic2).add_to(m)

    m.add_child(bm1)
    m.add_child(bm2)
    m._repr_html_()

    out = normalize(m._parent.render())

    # We verify that the script import is present.
    script = '<script src="https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.js"></script>'  # noqa
    assert script in out

    # We verify that the css import is present.
    css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.css"/>'  # noqa
    assert css in out

    # We verify that the Beautiful Icons are rendered correctly.
    tmpl = Template(
        """
                var {{this.get_name()}} = new L.BeautifyIcon.icon({{ this.options|tojavascript }})
                {{this._parent.get_name()}}.setIcon({{this.get_name()}});
            """
    )  # noqa

    assert normalize(tmpl.render(this=ic1)) in out
    assert normalize(tmpl.render(this=ic2)) in out
