# -*- coding: utf-8 -*-

""""
Folium Features Tests
---------------------

"""

import os
import warnings

from branca.element import Element

import folium
from folium import Map, Popup

from six import text_type


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


# Root path variable
rootpath = os.path.abspath(os.path.dirname(__file__))


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


def test_get_vegalite_major_version():
    spec_v2 = {'$schema': 'https://vega.github.io/schema/vega-lite/v2.6.0.json',
               'config': {'view': {'height': 300, 'width': 400}},
               'data': {'name': 'data-aac17e868e23f98b5e0830d45504be45'},
               'datasets': {'data-aac17e868e23f98b5e0830d45504be45': [{'folium usage': 0,
                                                                       'happiness': 1.0},
                                                                      {'folium usage': 1,
                                                                       'happiness': 2.718281828459045},
                                                                      {'folium usage': 2,
                                                                       'happiness': 7.38905609893065},
                                                                      {'folium usage': 3,
                                                                       'happiness': 20.085536923187668},
                                                                      {'folium usage': 4,
                                                                       'happiness': 54.598150033144236},
                                                                      {'folium usage': 5,
                                                                       'happiness': 148.4131591025766},
                                                                      {'folium usage': 6,
                                                                       'happiness': 403.4287934927351},
                                                                      {'folium usage': 7,
                                                                       'happiness': 1096.6331584284585},
                                                                      {'folium usage': 8,
                                                                       'happiness': 2980.9579870417283},
                                                                      {'folium usage': 9,
                                                                       'happiness': 8103.083927575384}]},
               'encoding': {'x': {'field': 'folium usage', 'type': 'quantitative'},
                            'y': {'field': 'happiness', 'type': 'quantitative'}},
               'mark': 'point'}

    vegalite_v2 = folium.features.VegaLite(spec_v2)

    assert vegalite_v2._get_vegalite_major_versions(spec_v2) == '2'

    spec_v1 = {'$schema': 'https://vega.github.io/schema/vega-lite/v1.3.1.json',
               'data': {'values': [{'folium usage': 0, 'happiness': 1.0},
                                   {'folium usage': 1, 'happiness': 2.718281828459045},
                                   {'folium usage': 2, 'happiness': 7.38905609893065},
                                   {'folium usage': 3, 'happiness': 20.085536923187668},
                                   {'folium usage': 4, 'happiness': 54.598150033144236},
                                   {'folium usage': 5, 'happiness': 148.4131591025766},
                                   {'folium usage': 6, 'happiness': 403.4287934927351},
                                   {'folium usage': 7, 'happiness': 1096.6331584284585},
                                   {'folium usage': 8, 'happiness': 2980.9579870417283},
                                   {'folium usage': 9, 'happiness': 8103.083927575384}]},
               'encoding': {'x': {'field': 'folium usage', 'type': 'quantitative'},
                            'y': {'field': 'happiness', 'type': 'quantitative'}},
               'height': 300,
               'mark': 'point',
               'width': 400}

    vegalite_v1 = folium.features.VegaLite(spec_v1)

    assert vegalite_v1._get_vegalite_major_versions(spec_v1) == '1'

    spec_no_version = {'config': {'view': {'height': 300, 'width': 400}},
                       'data': {'name': 'data-aac17e868e23f98b5e0830d45504be45'},
                       'datasets': {'data-aac17e868e23f98b5e0830d45504be45': [{'folium usage': 0,
                                                                               'happiness': 1.0},
                                                                              {'folium usage': 1,
                                                                               'happiness': 2.718281828459045},
                                                                              {'folium usage': 2,
                                                                               'happiness': 7.38905609893065},
                                                                              {'folium usage': 3,
                                                                               'happiness': 20.085536923187668},
                                                                              {'folium usage': 4,
                                                                               'happiness': 54.598150033144236},
                                                                              {'folium usage': 5,
                                                                               'happiness': 148.4131591025766},
                                                                              {'folium usage': 6,
                                                                               'happiness': 403.4287934927351},
                                                                              {'folium usage': 7,
                                                                               'happiness': 1096.6331584284585},
                                                                              {'folium usage': 8,
                                                                               'happiness': 2980.9579870417283},
                                                                              {'folium usage': 9,
                                                                               'happiness': 8103.083927575384}]},
                       'encoding': {'x': {'field': 'folium usage', 'type': 'quantitative'},
                                    'y': {'field': 'happiness', 'type': 'quantitative'}},
                       'mark': 'point'}

    vegalite_no_version = folium.features.VegaLite(spec_no_version)

    assert vegalite_no_version._get_vegalite_major_versions(spec_no_version) is None

# GeoJsonTooltip GeometryCollection
def test_geojson_tooltip():
    m = folium.Map([30.5, -97.5], zoom_start=10)
    folium.GeoJson(os.path.join(rootpath, "kuntarajat.geojson"),
                   tooltip=folium.GeoJsonTooltip(fields=['code', 'name'])
                   ).add_to(m)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        m._repr_html_()
        assert issubclass(w[-1].category, UserWarning), "GeoJsonTooltip GeometryCollection test failed."
