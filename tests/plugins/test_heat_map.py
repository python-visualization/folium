# -*- coding: utf-8 -*-
"""
Test HeatMap
------------
"""

from jinja2 import Template
import numpy as np

import folium
from folium import plugins


def test_heat_map():
    np.random.seed(3141592)
    data = (np.random.normal(size=(100, 2)) * np.array([[1, 1]]) +
            np.array([[48, 5]])).tolist()
    m = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
    hm = plugins.HeatMap(data)
    m.add_child(hm)
    m._repr_html_()

    out = m._parent.render()

    # We verify that the script import is present.
    script = '<script src="https://leaflet.github.io/Leaflet.heat/dist/leaflet-heat.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template("""
            var {{this.get_name()}} = L.heatLayer(
                {{this.data}},
                {
                    minOpacity: {{this.min_opacity}},
                    maxZoom: {{this.max_zoom}},
                    max: {{this.max_val}},
                    radius: {{this.radius}},
                    blur: {{this.blur}},
                    gradient: {{this.gradient}}
                    })
                .addTo({{this._parent.get_name()}});
    """)

    assert tmpl.render(this=hm)

    bounds = m.get_bounds()
    assert bounds == [[46.218566840847025, 3.0302801394447734],
                      [50.75345011431167, 7.132453997672826]], bounds
