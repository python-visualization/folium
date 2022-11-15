"""
Test Fullscreen
----------------

"""

import folium
from folium import plugins
from folium.utilities import normalize

from jinja2 import Template


def test_fullscreen():
    m = folium.Map([47, 3], zoom_start=1)
    fs = plugins.Fullscreen().add_to(m)

    out = normalize(m._parent.render())

    # verify that the fullscreen control was rendered
    tmpl = Template("""
        L.control.fullscreen(
            {{ this.options|tojson }}
        ).addTo({{this._parent.get_name()}});
    """)

    assert normalize(tmpl.render(this=fs)) in out
