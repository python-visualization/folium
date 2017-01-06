# -*- coding: utf-8 -*-
"""
Test TimestampedGeoJson
-----------------------
"""
from jinja2 import Template
import numpy as np

import folium
from folium import plugins


def test_timestamped_geo_json():
    coordinates = [[[[lon-8*np.sin(theta), -47+6*np.cos(theta)] for
                     theta in np.linspace(0, 2*np.pi, 25)],
                    [[lon-4*np.sin(theta), -47+3*np.cos(theta)] for theta
                     in np.linspace(0, 2*np.pi, 25)]] for
                   lon in np.linspace(-150, 150, 7)]
    data = {
        "type": "FeatureCollection",
        "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [0, 0],
                        },
                    "properties": {
                        "times": [1435708800000+12*86400000]
                        }
                    },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPoint",
                        "coordinates": [[lon, -25] for
                                        lon in np.linspace(-150, 150, 49)],
                        },
                    "properties": {
                        "times": [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 49)]
                        }
                    },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[lon, 25] for
                                        lon in np.linspace(-150, 150, 25)],
                        },
                    "properties": {
                        "times": [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 25)]
                        }
                    },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [[[lon-4*np.sin(theta),
                                          47+3*np.cos(theta)] for theta
                                         in np.linspace(0, 2*np.pi, 25)]
                                        for lon in
                                        np.linspace(-150, 150, 13)],
                        },
                    "properties": {
                        "times": [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 13)]
                        }
                    },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": coordinates,
                        },
                    "properties": {
                        "times": [1435708800000+i*86400000 for
                                  i in np.linspace(0, 25, 7)]
                        }
                    },
            ],
        }

    m = folium.Map([47, 3], zoom_start=1)
    tgj = plugins.TimestampedGeoJson(data)
    m.add_child(tgj)
    m._repr_html_()

    out = m._parent.render()

    # Verify the imports.
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/'
            'jquery.min.js"></script>'
            ) in out
    assert ('<script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/'
            '1.10.2/jquery-ui.min.js"></script>'
            ) in out
    assert ('<script src="https://rawgit.com/nezasa/'
            'iso8601-js-period/master/iso8601.min.js"></script>'
            ) in out
    assert ('<script src="https://rawgit.com/socib/Leaflet.'
            'TimeDimension/master/dist/leaflet.timedimension.min.js">'
            '</script>'
            ) in out
    assert ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/'
            'libs/highlight.js/8.4/styles/default.min.css" />'
            ) in out
    assert ('<link rel="stylesheet" href="http://apps.socib.es/Leaflet.'
            'TimeDimension/dist/leaflet.timedimension.control.min.css" />'
            ) in out

    # Verify that the script is okay.
    tmpl = Template("""
        {{this._parent.get_name()}}.timeDimension = L.timeDimension({period:"{{this.period}}"});
        {{this._parent.get_name()}}.timeDimensionControl = L.control.timeDimension({
            position: 'bottomleft',
            autoPlay: {{'true' if this.auto_play else 'false'}},
            playerOptions: {
                transitionTime: {{this.transition_time}},
                loop: {{'true' if this.loop else 'false'}}}
                });
        {{this._parent.get_name()}}.addControl({{this._parent.get_name()}}.timeDimensionControl);

        var {{this.get_name()}} = L.timeDimension.layer.geoJson(
            L.geoJson({{this.data}}),
            {updateTimeDimension: true,addlastPoint: true}
            ).addTo({{this._parent.get_name()}});
    """)  # noqa

    assert ''.join(tmpl.render(this=tgj).split()) in ''.join(out.split())

    bounds = m.get_bounds()
    assert bounds == [[-53.0, -158.0], [50.0, 158.0]], bounds
