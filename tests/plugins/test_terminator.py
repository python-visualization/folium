# -*- coding: utf-8 -*-
"""
Test Terminator
---------------
"""

from jinja2 import Template

import folium
from folium import plugins


def test_terminator():
    m = folium.Map([45., 3.], zoom_start=1)
    t = plugins.Terminator()
    m.add_child(t)
    m._repr_html_()

    out = m._parent.render()

    # Verify that the script is okay.
    tmpl = Template('L.terminator().addTo({{this._parent.get_name()}});')
    assert ''.join(tmpl.render(this=t).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
