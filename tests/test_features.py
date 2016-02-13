# -*- coding: utf-8 -*-
""""
Folium Features Tests
---------------------

"""

import os

from branca.six import text_type
from branca.element import Element

from folium import Map, Popup
from folium import features

tmpl = """
        <!DOCTYPE html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
            <script src="https://rawgithub.com/lvoogdt/Leaflet.awesome-markers/2.0/develop/dist/leaflet.awesome-markers.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster-src.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" />
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" />
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css" />
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" />
            <link rel="stylesheet" href="https://rawgit.com/lvoogdt/Leaflet.awesome-markers/2.0/develop/dist/leaflet.awesome-markers.css" />
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css" />
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css" />
            <link rel="stylesheet" href="https://raw.githubusercontent.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css" />
            <style>
            html, body {
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
                }
            #map {
                position:absolute;
                top:0;
                bottom:0;
                right:0;
                left:0;
                }
            </style>
        </head>
        <body>
        </body>
        <script>
        </script>
"""  # noqa


# Figure
def test_figure_creation():
    f = features.Figure()
    assert isinstance(f, Element)

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_rendering():
    f = features.Figure()
    out = f.render()
    assert type(out) is text_type

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_html():
    f = features.Figure()
    out = f.render()
    out = os.linesep.join([s for s in out.splitlines() if s.strip()])
    print(out)
    assert out.strip() == tmpl.strip()

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_double_rendering():
    f = features.Figure()
    out = f.render()
    out2 = f.render()
    assert out == out2

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_marker_popups():
    m = Map()
    features.Marker([45, -180], popup='-180').add_to(m)
    features.Marker([45, -120], popup=Popup('-120')).add_to(m)
    features.RegularPolygonMarker([45, -60], popup='-60').add_to(m)
    features.RegularPolygonMarker([45, 0], popup=Popup('0')).add_to(m)
    features.CircleMarker([45, 60], popup='60').add_to(m)
    features.CircleMarker([45, 120], popup=Popup('120')).add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[45, -180], [45, 120]], bounds


def test_polyline_popups():
    m = Map([43, -100], zoom_start=4)
    features.PolyLine([[40, -80], [45, -80]], popup="PolyLine").add_to(m)
    features.PolyLine([[40, -90], [45, -90]],
                      popup=Popup("PolyLine")).add_to(m)
    features.MultiPolyLine([[[40, -110], [45, -110]]],
                           popup="MultiPolyLine").add_to(m)
    features.MultiPolyLine([[[40, -120], [45, -120]]],
                           popup=Popup("MultiPolyLine")).add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[40, -120], [45, -80]], bounds


# DivIcon.
def test_divicon():
    html = """<svg height="100" width="100">
              <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
              </svg>"""  # noqa
    div = features.DivIcon(html=html)
    assert isinstance(div, Element)
    assert div.className == 'empty'
    assert div.html == html


# WmsTileLayer.
def test_wms_service():
    m = Map([40, -100], zoom_start=4)
    url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
    w = features.WmsTileLayer(url,
                              name='test',
                              format='image/png',
                              layers='nexrad-n0r-900913',
                              attr=u"Weather data © 2012 IEM Nexrad",
                              transparent=True)
    w.add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds
