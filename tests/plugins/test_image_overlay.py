# -*- coding: utf-8 -*-
"""
Test ImageOverlay
-----------------

"""

from jinja2 import Template

import folium
from folium import plugins


def test_image_overlay():
    """Test image overlay."""
    data = [[[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[1, 1, 0, 0.5], [0, 0, 1, 1], [0, 0, 1, 1]]]

    m = folium.Map()
    io = plugins.ImageOverlay(data, [[0, -180], [90, 180]],
                              mercator_project=True)
    io.add_to(m)
    m._repr_html_()

    out = m._parent.render()

    # Verify the URL generation.
    url = ('data:image/png;base64,'
           'iVBORw0KGgoAAAANSUhEUgAAAAMAAAACCAYAAACddGYaAAA'
           'AF0lEQVR42mP4z8AARFDw/z/DeiA5H4QBV60H6ABl9ZIAAAAASUVORK5CYII=')
    assert io.url == url

    # Verify the script part is okay.
    tmpl = Template("""
                var {{this.get_name()}} = L.imageOverlay(
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
    """)
    assert tmpl.render(this=io) in out

    bounds = m.get_bounds()
    assert bounds == [[0, -180], [90, 180]], bounds
