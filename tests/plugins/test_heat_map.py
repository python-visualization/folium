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
    tmpl = Template("""
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
    """)

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


def test_heatmap_integer_numpy_weights():
    """Integer numpy arrays of shape (n, 3) are documented as supported input.

    ``np.float64`` is a subclass of ``float`` so JSON serialization tolerates
    float weights, but ``np.int64`` is not a subclass of ``int``, so an
    all-integer array (dtype ``int64``) used to crash rendering with
    "Object of type int64 is not JSON serializable". The weight column must be
    coerced to ``float`` the same way ``validate_location`` coerces lat/lon.
    """
    data = np.array([[3, 4, 1], [5, 6, 2]])
    assert data.dtype == np.int64

    hm = HeatMap(data)

    # Weights must be normalized to plain Python floats, matching lat/lon.
    for point in hm.data:
        assert len(point) == 3
        for value in point:
            assert type(value) is float

    # Rendering must not raise (the JSON serialization used to fail here).
    m = folium.Map()
    hm.add_to(m)
    out = m.get_root().render()
    assert "L.heatLayer" in out

    # Integer and float weights must produce identical serialized data.
    hm_float = HeatMap(np.array([[3, 4, 1.0], [5, 6, 2.0]]))
    assert hm.data == hm_float.data


def test_heatmap_integer_numpy_no_weight():
    """Integer numpy arrays of shape (n, 2) (no weight column) also render."""
    data = np.array([[3, 4], [5, 6]])
    assert data.dtype == np.int64
    m = folium.Map()
    HeatMap(data).add_to(m)
    assert "L.heatLayer" in m.get_root().render()
