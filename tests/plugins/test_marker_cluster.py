# -*- coding: utf-8 -*-

"""
Test MarkerCluster
------------------
"""

import folium
from folium import plugins
from folium.utilities import normalize

from jinja2 import Template

import numpy as np


def test_marker_cluster():
    N = 100
    np.random.seed(seed=26082009)
    data = np.array([
        np.random.uniform(low=35, high=60, size=N),   # Random latitudes.
        np.random.uniform(low=-12, high=30, size=N),  # Random longitudes.
    ]).T
    m = folium.Map([45., 3.], zoom_start=4)
    mc = plugins.MarkerCluster(data).add_to(m)

    out = normalize(m._parent.render())

    # We verify that imports
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css"/>' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css"/>' in out  # noqa

    # Verify the script part is okay.
    tmpl = Template("""
        var {{this.get_name()}} = L.markerClusterGroup(
            {{ this.options|tojson }}
        );
        {%- if this.icon_create_function is not none %}
            {{ this.get_name() }}.options.iconCreateFunction =
                {{ this.icon_create_function.strip() }};
            {%- endif %}
        {{this._parent.get_name()}}.addLayer({{this.get_name()}});

        {% for marker in this._children.values() %}
            var {{marker.get_name()}} = L.marker(
                {{ marker.location|tojson }},
                {}
            ).addTo({{this.get_name()}});
        {% endfor %}
    """)
    expected = normalize(tmpl.render(this=mc))
    assert expected in out

    bounds = m.get_bounds()
    np.testing.assert_allclose(
        bounds,
        [[35.147332572663785, -11.520684337300109],
         [59.839718052359274, 29.94931046497927]])
