"""
Test HeatMap
------------
"""

import numpy as np
import pytest

import folium
from folium.plugins import HeatMap
from folium.template import Template
from folium.utilities import normalize


def test_heat_map():
    np.random.seed(3141592)
    data = np.random.normal(size=(100, 2)) * np.array([[1, 1]]) + np.array([[48, 5]])
    m = folium.Map([48.0, 5.0], zoom_start=6)
    hm = HeatMap(data)
    m.add_child(hm)
    m._repr_html_()

    out = normalize(m._parent.render())

    # We verify that the script import is present.
    script = '<script src="https://cdn.jsdelivr.net/gh/python-visualization/folium@main/folium/templates/leaflet_heat.min.js"></script>'  # noqa
    assert script in out

    # We verify that the script part is correct.
    tmpl = Template(
        """
            var {{this.get_name()}} = L.heatLayer(
                {{this.data}},
                {
                    minOpacity: {{this.min_opacity}},
                    maxZoom: {{this.max_zoom}},
                    radius: {{this.radius}},
                    blur: {{this.blur}},
                    gradient: {{this.gradient}}
                    })
                .addTo({{this._parent.get_name()}});
    """
    )

    assert tmpl.render(this=hm)

    bounds = m.get_bounds()
    np.testing.assert_allclose(
        bounds,
        [
            [46.218566840847025, 3.0302801394447734],
            [50.75345011431167, 7.132453997672826],
        ],
    )


def test_heatmap_data():
    data = HeatMap(np.array([[3, 4, 1], [5, 6, 1], [7, 8, 0.5]])).data
    assert isinstance(data, list)
    assert len(data) == 3
    for i in range(len(data)):
        assert isinstance(data[i], list)
        assert len(data[i]) == 3


def test_heat_map_exception():
    with pytest.raises(ValueError):
        HeatMap(np.array([[4, 5, 1], [3, 6, np.nan]]))
    with pytest.raises(Exception):
        HeatMap(np.array([3, 4, 5]))
