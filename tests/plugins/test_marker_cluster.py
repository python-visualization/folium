"""
Test MarkerCluster
------------------
"""

import numpy as np
from jinja2 import Template

import folium
from folium import plugins
from folium.utilities import normalize


def test_marker_cluster():
    N = 100
    np.random.seed(seed=26082009)
    data = np.array(
        [
            np.random.uniform(low=35, high=60, size=N),  # Random latitudes.
            np.random.uniform(low=-12, high=30, size=N),  # Random longitudes.
        ]
    ).T
    m = folium.Map([45.0, 3.0], zoom_start=4)
    mc = plugins.MarkerCluster(data).add_to(m)

    tmpl_for_expected = Template(
        """
        var {{this.get_name()}} = L.markerClusterGroup(
            {{ this.options|tojson }}
        );
        {%- if this.icon_create_function is not none %}
            {{ this.get_name() }}.options.iconCreateFunction =
                {{ this.icon_create_function.strip() }};
            {%- endif %}

        {% for marker in this._children.values() %}
            var {{marker.get_name()}} = L.marker(
                {{ marker.location|tojson }},
                {}
            ).addTo({{this.get_name()}});
        {% endfor %}

        {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
    """
    )
    expected = normalize(tmpl_for_expected.render(this=mc))

    out = normalize(m._parent.render())

    # We verify that imports
    assert (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>'  # noqa
        in out
    )  # noqa
    assert (
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css"/>'  # noqa
        in out
    )  # noqa
    assert (
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css"/>'  # noqa
        in out
    )  # noqa

    assert expected in out

    bounds = m.get_bounds()
    np.testing.assert_allclose(
        bounds,
        [
            [35.147332572663785, -11.520684337300109],
            [59.839718052359274, 29.94931046497927],
        ],
    )
