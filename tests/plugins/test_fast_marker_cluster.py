# -*- coding: utf-8 -*-

"""
Test FastMarkerCluster
------------------
"""

from __future__ import (absolute_import, division, print_function)

import folium

from folium import plugins

from jinja2 import Template

import numpy as np


def test_fast_marker_cluster():
    n = 100
    np.random.seed(seed=26082009)
    data = np.array([
        np.random.uniform(low=35, high=60, size=n),   # Random latitudes.
        np.random.uniform(low=-12, high=30, size=n),  # Random longitudes.
        range(n),                                     # Popups.
    ]).tolist()
    m = folium.Map([45., 3.], zoom_start=4)
    mc = plugins.FastMarkerCluster(data, callback=None)
    m.add_child(mc)
    m._repr_html_()

    out = m._parent.render()

    # We verify that imports
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css" />' in out  # noqa
    assert '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css" />' in out  # noqa

    # Verify the script part is okay.
    tmpl = Template("""
        {% macro script(this, kwargs) %}
        (function() {
            var data = {{this._data}};
            var map = {{this._parent.get_name()}};
            var cluster = L.markerClusterGroup();
            {{this._callback}}

            for (var i = 0; i < data.length; i++) {
                var row = data[i];
                var marker = callback(row, popup='names');
                marker.addTo(cluster);
            }

            cluster.addTo(map);
        })();
        {% endmacro %}
    """)

    assert ''.join(tmpl.render(this=mc).split()) in ''.join(out.split())
