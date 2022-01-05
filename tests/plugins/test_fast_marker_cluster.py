"""
Test FastMarkerCluster
----------------------
"""

import folium
from folium.plugins import FastMarkerCluster
from folium.utilities import normalize

from jinja2 import Template

import numpy as np

import pandas as pd

import pytest


def test_fast_marker_cluster():
    n = 100
    np.random.seed(seed=26082009)
    data = np.array([
        np.random.uniform(low=35, high=60, size=n),
        np.random.uniform(low=-12, high=30, size=n),
    ]).T
    m = folium.Map([45., 3.], zoom_start=4)
    mc = FastMarkerCluster(data).add_to(m)

    out = normalize(m._parent.render())

    # We verify that imports
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css"/>' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css"/>' in out  # noqa

    # Verify the script part is okay.
    tmpl = Template("""
        var {{ this.get_name() }} = (function(){
            {{ this.callback }}

            var data = {{ this.data|tojson }};
            var cluster = L.markerClusterGroup({{ this.options|tojson }});
            {%- if this.icon_create_function is not none %}
            cluster.options.iconCreateFunction =
                {{ this.icon_create_function.strip() }};
            {%- endif %}

            for (var i = 0; i < data.length; i++) {
                var row = data[i];
                var marker = callback(row);
                marker.addTo(cluster);
            }

            cluster.addTo({{ this._parent.get_name() }});
            return cluster;
        })();
    """)
    expected = normalize(tmpl.render(this=mc))
    assert expected in out


@pytest.mark.parametrize('case', [
    np.array([[0, 5, 1], [1, 6, 1], [2, 7, 0.5]]),
    [[0, 5, 'red'], (1, 6, 'blue'), [2, 7, {'this': 'also works'}]],
    pd.DataFrame([[0, 5, 'red'], [1, 6, 'blue'], [2, 7, 'something']],
                 columns=['lat', 'lng', 'color']),
])
def test_fast_marker_cluster_data(case):
    data = FastMarkerCluster(case).data
    assert isinstance(data, list)
    assert len(data) == 3
    for i in range(len(data)):
        assert isinstance(data[i], list)
        assert len(data[i]) == 3
        assert data[i][0] == float(i)
        assert data[i][1] == float(i + 5)
