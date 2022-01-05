"""
Test Terminator
---------------
"""

import folium
from folium import plugins
from folium.utilities import normalize

from jinja2 import Template


def test_terminator():
    m = folium.Map([45., 3.], zoom_start=1)
    t = plugins.Terminator().add_to(m)

    out = normalize(m._parent.render())

    # Verify that the script is okay.
    tmpl = Template('L.terminator().addTo({{this._parent.get_name()}});')
    expected = normalize(tmpl.render(this=t))
    assert expected in out

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
