# -*- coding: utf-8 -*-

""""
Circle and Circle Marker Features
---------------------------------

"""

from __future__ import (absolute_import, division, print_function)

import json

from folium import Map
from folium.features import Circle, CircleMarker


def test_circle():
    m = Map()
    radius = 10000
    popup = 'I am {} meters'.format(radius)

    circle = Circle(
        location=[-27.551667, -48.478889],
        radius=radius,
        color='black',
        weight=2,
        fill_opacity=0.6,
        opacity=1,
        fill=True,
        popup=popup,
    )
    circle.add_to(m)

    options = {
        'bubblingMouseEvents': True,
        'color': 'black',
        'dashArray': None,
        'dashOffset': None,
        'fill': True,
        'fillColor': 'black',
        'fillOpacity': 0.6,
        'fillRule': 'evenodd',
        'lineCap': 'round',
        'lineJoin': 'round',
        'opacity': 1,
        'radius': 10000,
        'stroke': True,
        'weight': 2,
    }

    m._repr_html_()
    expected_bounds = [[-27.551667, -48.478889], [-27.551667, -48.478889]]
    expected_rendered = """
    var {0} = L.circle(
    [-27.551667,-48.478889],
    {{
    "bubblingMouseEvents": true,
    "color": "black",
    "dashArray": null,
    "dashOffset": null,
    "fill": true,
    "fillColor": "black",
    "fillOpacity": 0.6,
    "fillRule": "evenodd",
    "lineCap": "round",
    "lineJoin": "round",
    "opacity": 1,
    "radius": 10000,
    "stroke": true,
    "weight": 2
    }}
    ).addTo({1});
    """.format(circle.get_name(), m.get_name())

    rendered = circle._template.module.script(circle)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert circle.get_bounds() == expected_bounds
    assert json.dumps(circle.to_dict()) == circle.to_json()
    assert circle.location == [-27.551667, -48.478889]
    assert circle.options == json.dumps(options, sort_keys=True, indent=2)


def test_circle_marker():
    m = Map()
    radius = 50
    popup = 'I am {} pixels'.format(radius)

    circle_marker = CircleMarker(
        location=[-27.55, -48.8],
        radius=radius,
        color='black',
        weight=2,
        fill_opacity=0.6,
        opacity=1,
        fill=True,
        popup=popup,
    )
    circle_marker.add_to(m)

    options = {
        'bubblingMouseEvents': True,
        'color': 'black',
        'dashArray': None,
        'dashOffset': None,
        'fill': True,
        'fillColor': 'black',
        'fillOpacity': 0.6,
        'fillRule': 'evenodd',
        'lineCap': 'round',
        'lineJoin': 'round',
        'opacity': 1,
        'radius': 50,
        'stroke': True,
        'weight': 2,
    }

    m._repr_html_()
    expected_bounds = [[-27.55, -48.8], [-27.55, -48.8]]
    expected_rendered = """
    var {0} = L.circleMarker(
    [-27.55,-48.8],
    {{
    "bubblingMouseEvents": true,
    "color": "black",
    "dashArray": null,
    "dashOffset": null,
    "fill": true,
    "fillColor": "black",
    "fillOpacity": 0.6,
    "fillRule": "evenodd",
    "lineCap": "round",
    "lineJoin": "round",
    "opacity": 1,
    "radius": 50,
    "stroke": true,
    "weight": 2
    }}
    ).addTo({1});
    """.format(circle_marker.get_name(), m.get_name())

    rendered = circle_marker._template.module.script(circle_marker)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert circle_marker.get_bounds() == expected_bounds
    assert json.dumps(circle_marker.to_dict()) == circle_marker.to_json()
    assert circle_marker.location == [-27.55, -48.8]
    assert circle_marker.options == json.dumps(options, sort_keys=True, indent=2)
