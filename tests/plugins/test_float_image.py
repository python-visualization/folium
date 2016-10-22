# -*- coding: utf-8 -*-
"""
Test FloatImage
---------------
"""

from jinja2 import Template

import folium
from folium import plugins


def test_float_image():
    m = folium.Map([45., 3.], zoom_start=4)
    url = 'https://raw.githubusercontent.com/SECOORA/static_assets/master/maps/img/rose.png'
    szt = plugins.FloatImage(url, bottom=60, left=70)
    m.add_child(szt)
    m._repr_html_()

    out = m._parent.render()

    # Verify that the div has been created.
    tmpl = Template("""
        <img id="{{this.get_name()}}" alt="float_image"
        src="https://raw.githubusercontent.com/SECOORA/static_assets/master/maps/img/rose.png"
        style="z-index: 999999">
        </img>
    """)
    assert ''.join(tmpl.render(this=szt).split()) in ''.join(out.split())

    # Verify that the style has been created.
    tmpl = Template("""
        <style>
            #{{this.get_name()}} {
                position:absolute;
                bottom:60%;
                left:70%;
                }
        </style>
    """)
    assert ''.join(tmpl.render(this=szt).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
