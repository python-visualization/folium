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
    out = os.linesep.join([s.strip() for s in out.splitlines() if s.strip()])
    print(out)
    assert out.strip() == tmpl.strip(), '\n' + out.strip() + '\n' + '-' * 80 + '\n' + tmpl.strip()  # noqa

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
    features.CircleMarker([45, 90], popup=Popup('90'), weight=0).add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[45, -180], [45, 120]], bounds


def test_polyline_popups():
    m = Map([43, -100], zoom_start=4)
    features.PolyLine([[40, -80], [45, -80]], popup="PolyLine").add_to(m)
    features.PolyLine([[40, -90], [45, -90]],
                      popup=Popup("PolyLine")).add_to(m)
    features.PolyLine([[[40, -110], [45, -110]]],
                      popup="MultiPolyLine").add_to(m)
    features.PolyLine([[[40, -120], [45, -120]]],
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


# ColorLine.
def test_color_line():
    m = Map([22.5, 22.5], zoom_start=3)
    color_line = features.ColorLine(
        [[0, 0], [0, 45], [45, 45], [45, 0], [0, 0]],
        [0, 1, 2, 3],
        colormap=['b', 'g', 'y', 'r'],
        nb_steps=4,
        weight=10,
        opacity=1)
    m.add_child(color_line)
    m._repr_html_()
