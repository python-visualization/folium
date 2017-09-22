# -*- coding: utf-8 -*-

""""
Folium Features Tests
---------------------

"""

from __future__ import (absolute_import, division, print_function)

import os

from branca.element import Element
from branca.six import text_type

from folium import Map, Popup
import folium

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
    f = folium.Figure()
    assert isinstance(f, Element)

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_rendering():
    f = folium.Figure()
    out = f.render()
    assert type(out) is text_type

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_html():
    f = folium.Figure()
    out = f.render()
    out = os.linesep.join([s.strip() for s in out.splitlines() if s.strip()])
    assert out.strip() == tmpl.strip(), '\n' + out.strip() + '\n' + '-' * 80 + '\n' + tmpl.strip()  # noqa

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_double_rendering():
    f = folium.Figure()
    out = f.render()
    out2 = f.render()
    assert out == out2

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_marker_popups():
    m = Map()
    folium.Marker([45, -180], popup='-180').add_to(m)
    folium.Marker([45, -120], popup=Popup('-120')).add_to(m)
    folium.RegularPolygonMarker([45, -60], popup='-60').add_to(m)
    folium.RegularPolygonMarker([45, 0], popup=Popup('0')).add_to(m)
    folium.CircleMarker([45, 60], popup='60').add_to(m)
    folium.CircleMarker([45, 120], popup=Popup('120')).add_to(m)
    folium.CircleMarker([45, 90], popup=Popup('90'), weight=0).add_to(m)
    m._repr_html_()

    bounds = m.get_bounds()
    assert bounds == [[45, -180], [45, 120]], bounds


# DivIcon.
def test_divicon():
    html = """<svg height="100" width="100">
              <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
              </svg>"""  # noqa
    div = folium.DivIcon(html=html)
    assert isinstance(div, Element)
    assert div.className == 'empty'
    assert div.html == html


# ColorLine.
def test_color_line():
    m = Map([22.5, 22.5], zoom_start=3)
    color_line = folium.ColorLine(
        [[0, 0], [0, 45], [45, 45], [45, 0], [0, 0]],
        [0, 1, 2, 3],
        colormap=['b', 'g', 'y', 'r'],
        nb_steps=4,
        weight=10,
        opacity=1)
    m.add_child(color_line)
    m._repr_html_()
