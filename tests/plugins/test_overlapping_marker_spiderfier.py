"""
Test OverlappingMarkerSpiderfier
--------------------------------
"""

import numpy as np
from jinja2 import Template

import folium
from folium import plugins
from folium.utilities import normalize


def test_overlapping_marker_spiderfier():
    N = 10
    np.random.seed(seed=26082009)
    data = np.array(
        [
            np.random.uniform(low=45.0, high=45.1, size=N),
            np.random.uniform(low=3.0, high=3.1, size=N),
        ]
    ).T

    m = folium.Map([45.05, 3.05], zoom_start=14)
    markers = [
        folium.Marker(location=loc, popup=f"Marker {i}") for i, loc in enumerate(data)
    ]

    for marker in markers:
        marker.add_to(m)

    oms = plugins.OverlappingMarkerSpiderfier(
        markers=markers, options={"keepSpiderfied": True, "nearbyDistance": 20}
    ).add_to(m)

    tmpl_for_expected = Template(
        """
        var {{this.get_name()}} = (function () {
            var layerGroup = L.layerGroup();
            try {
                var oms = new OverlappingMarkerSpiderfier(
                    {{ this._parent.get_name() }},
                    {{ this.options|tojson }}
                );

                var popup = L.popup({
                    offset: L.point(0, -30)
                });

                oms.addListener('click', function(marker) {
                    var content;
                    if (marker.options && marker.options.options && marker.options.options.desc) {
                        content = marker.options.options.desc;
                    } else if (marker._popup && marker._popup._content) {
                        content = marker._popup._content;
                    } else {
                        content = "";
                    }

                    if (content) {
                        popup.setContent(content);
                        popup.setLatLng(marker.getLatLng());
                        {{ this._parent.get_name() }}.openPopup(popup);
                    }
                });

                oms.addListener('spiderfy', function(markers) {
                    {{ this._parent.get_name() }}.closePopup();
                });

                {% for marker in this.markers %}
                var {{ marker.get_name() }} = L.marker(
                    {{ marker.location|tojson }},
                    {{ marker.options|tojson }}
                );

                {% if marker.popup %}
                {{ marker.get_name() }}.bindPopup({{ marker.popup.get_content()|tojson }});
                {% endif %}

                oms.addMarker({{ marker.get_name() }});
                layerGroup.addLayer({{ marker.get_name() }});
                {% endfor %}
            } catch (error) {
                console.error('Error in OverlappingMarkerSpiderfier initialization:', error);
            }

            return layerGroup;
        })();
        """
    )
    expected = normalize(tmpl_for_expected.render(this=oms))

    out = normalize(m._parent.render())

    assert (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/OverlappingMarkerSpiderfier-Leaflet/0.2.6/oms.min.js"></script>'
        in out
    )

    assert expected in out

    bounds = m.get_bounds()
    assert bounds is not None, "Map bounds should not be None"

    min_lat, min_lon = data.min(axis=0)
    max_lat, max_lon = data.max(axis=0)

    assert bounds[0][0] <= min_lat
    assert bounds[0][1] <= min_lon
    assert bounds[1][0] >= max_lat
    assert bounds[1][1] >= max_lon
