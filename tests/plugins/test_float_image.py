"""
Test FloatImage
---------------
"""

import folium
from folium import plugins
from folium.template import Template
from folium.utilities import normalize


def test_float_image():
    m = folium.Map([45.0, 3.0], zoom_start=4)
    url = "https://raw.githubusercontent.com/SECOORA/static_assets/master/maps/img/rose.png"
    szt = plugins.FloatImage(url, bottom=60, left=70, width="20%")
    m.add_child(szt)
    m._repr_html_()

    out = normalize(m._parent.render())

    # Verify that the div has been created.
    tmpl = Template(
        """
        <img id="{{this.get_name()}}" alt="float_image"
        src="https://raw.githubusercontent.com/SECOORA/static_assets/master/maps/img/rose.png"
        style="z-index: 999999">
        </img>
    """
    )
    assert normalize(tmpl.render(this=szt)) in out

    # Verify that the style has been created.
    tmpl = Template(
        """
        <style>
            #{{this.get_name()}} {
                position: absolute;
                bottom: 60%;
                left: 70%;
                width: 20%;
                }
        </style>
    """
    )
    assert normalize(tmpl.render(this=szt)) in out

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
