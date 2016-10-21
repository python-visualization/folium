# -*- coding: utf-8 -*-
"""
Test MarkerCluster
------------------
"""

from jinja2 import Template
import numpy as np

import folium
from folium import plugins


def test_marker_cluster():
    N = 100
    np.random.seed(seed=26082009)
    data = np.array([
        np.random.uniform(low=35, high=60, size=N),   # Random latitudes.
        np.random.uniform(low=-12, high=30, size=N),  # Random longitudes.
        range(N),                                     # Popups.
        ]).T
    m = folium.Map([45., 3.], zoom_start=4)
    mc = plugins.MarkerCluster(data)
    m.add_child(mc)
    m._repr_html_()

    out = m._parent.render()

    # We verify that imports
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.'
            'markercluster/1.0.0/leaflet.markercluster.js"></script>') in out
    assert ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/'
            'libs/leaflet.markercluster/1.0.0/MarkerCluster.css" />') in out
    assert ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/'
            'libs/leaflet.markercluster/1.0.0/MarkerCluster.Default.css" />'
            ) in out

    # Verify the script part is okay.
    tmpl = Template("""
        var {{this.get_name()}} = L.markerClusterGroup();
        {{this._parent.get_name()}}.addLayer({{this.get_name()}});

        {% for marker in this._children.values() %}
            var {{marker.get_name()}} = L.marker(
                [{{marker.location[0]}},{{marker.location[1]}}],
                {
                    icon: new L.Icon.Default()
                    }
                )
                .addTo({{this.get_name()}});
        {% endfor %}
    """)
    assert ''.join(tmpl.render(this=mc).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[35.147332572663785, -11.520684337300109],
                      [59.839718052359274, 29.94931046497927]], bounds
