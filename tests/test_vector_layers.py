# -*- coding: utf-8 -*-

""""
Test Vector Layers
------------------

"""

from __future__ import (absolute_import, division, print_function)

import json

from folium import Map
from folium.features import Circle, CircleMarker, Polygon, Rectangle
from folium.utilities import get_bounds


def test_circle():
    m = Map()
    radius = 10000
    popup = 'I am {} meters'.format(radius)
    location = [-27.551667, -48.478889]

    circle = Circle(
        location=location,
        radius=radius,
        color='black',
        weight=2,
        fill_opacity=0.6,
        opacity=1,
        fill=True,
        popup=popup,
    )
    circle.add_to(m)

    expected_options = {
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
        'radius': radius,
        'stroke': True,
        'weight': 2,
    }

    m._repr_html_()
    expected_rendered = """
    var {name} = L.circle(
    {location},
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
    "radius": {radius},
    "stroke": true,
    "weight": 2
    }}
    )
    .addTo({map});
    """.format(name=circle.get_name(), location=location, radius=radius, map=m.get_name())  # noqa

    rendered = circle._template.module.script(circle)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert circle.get_bounds() == [location, location]
    assert json.dumps(circle.to_dict()) == circle.to_json()
    assert circle.location == [-27.551667, -48.478889]
    assert circle.options == json.dumps(expected_options, sort_keys=True, indent=2)  # noqa


def test_circle_marker():
    m = Map()
    radius = 50
    popup = 'I am {} pixels'.format(radius)
    location = [-27.55, -48.8]

    circle_marker = CircleMarker(
        location=location,
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
        'radius': radius,
        'stroke': True,
        'weight': 2,
    }

    m._repr_html_()
    expected_bounds = [location, location]
    expected_rendered = """
    var {name} = L.circleMarker(
    {location},
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
    "radius": {radius},
    "stroke": true,
    "weight": 2
    }}
    )
    .addTo({map});
    """.format(name=circle_marker.get_name(), location=location, radius=radius, map=m.get_name())  # noqa

    rendered = circle_marker._template.module.script(circle_marker)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert circle_marker.get_bounds() == expected_bounds
    assert json.dumps(circle_marker.to_dict()) == circle_marker.to_json()
    assert circle_marker.location == location
    assert circle_marker.options == json.dumps(options, sort_keys=True, indent=2)  # noqa


def test_rectangle():
    m = Map()

    location = [[45.6, -122.8], [45.61, -122.7]]
    rectangle = Rectangle(
        bounds=location,
        popup='I am a rectangle',
        color='black',
        weight=2,
        fill_opacity=0.6,
        opacity=1,
        fill=True,
        )
    rectangle.add_to(m)

    expected_options = {
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
        'stroke': True,
        'weight': 2,
    }

    m._repr_html_()
    expected_rendered = """
    var {name} = L.rectangle(
    {location},
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
    "stroke": true,
    "weight": 2
    }}
    )
    .addTo({map});
    """.format(name=rectangle.get_name(), location=location, map=m.get_name())

    rendered = rectangle._template.module.script(rectangle)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert rectangle.get_bounds() == location
    assert json.dumps(rectangle.to_dict()) == rectangle.to_json()
    assert rectangle.options == json.dumps(expected_options, sort_keys=True, indent=2)  # noqa


def test_polygon_marker():
    m = Map()
    locations = [[35.6636, 139.7634],
                 [35.6629, 139.7664],
                 [35.6663, 139.7706],
                 [35.6725, 139.7632],
                 [35.6728, 139.7627],
                 [35.6720, 139.7606],
                 [35.6682, 139.7588],
                 [35.6663, 139.7627]]
    polygon = Polygon(locations=locations, popup='I am a polygon')
    polygon.add_to(m)

    expected_options = {
        'bubblingMouseEvents': True,
        'color': '#3388ff',
        'dashArray': None,
        'dashOffset': None,
        'fill': True,
        'fillColor': '#3388ff',
        'fillOpacity': 0.2,
        'fillRule': 'evenodd',
        'lineCap': 'round',
        'lineJoin': 'round',
        'opacity': 1.0,
        'stroke': True,
        'weight': 3,
    }

    m._repr_html_()
    expected_rendered = """
    var {name} = L.polygon(
    {locations},
    {{
    "bubblingMouseEvents": true,
    "color": "#3388ff",
    "dashArray": null,
    "dashOffset": null,
    "fill": true,
    "fillColor": "#3388ff",
    "fillOpacity": 0.2,
    "fillRule": "evenodd",
    "lineCap": "round",
    "lineJoin": "round",
    "opacity": 1.0,
    "stroke": true,
    "weight": 3
    }}
    )
    .addTo({map});
    """.format(locations=locations, name=polygon.get_name(), map=m.get_name())

    rendered = polygon._template.module.script(polygon)
    assert rendered.strip().split() == expected_rendered.strip().split()
    assert polygon.get_bounds() == get_bounds(locations)
    assert json.dumps(polygon.to_dict()) == polygon.to_json()
    assert polygon.options == json.dumps(expected_options, sort_keys=True, indent=2)  # noqa
