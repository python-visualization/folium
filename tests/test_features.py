""""
Folium Features Tests
---------------------

"""

import os
import warnings

import json

from branca.element import Element

import folium
from folium import Map, Popup, GeoJson, ClickForMarker

import pytest


@pytest.fixture
def tmpl():
    yield ("""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    </head>
    <body>
    </body>
    <script>
    </script>
    </html>
    """)  # noqa


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
    assert type(out) is str

    bounds = f.get_bounds()
    assert bounds == [[None, None], [None, None]], bounds


def test_figure_html(tmpl):
    f = folium.Figure()
    out = f.render()
    out = os.linesep.join([s.strip() for s in out.splitlines() if s.strip()])
    tmpl = os.linesep.join([s.strip() for s in tmpl.splitlines() if s.strip()])
    assert out == tmpl, '\n' + out + '\n' + '-' * 80 + '\n' + tmpl

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
    assert div.options['className'] == 'empty'
    assert div.options['html'] == html


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


@pytest.fixture
def vegalite_spec(version):
    file_version = 'v1' if version == 1 else 'vlater'
    file = os.path.join(rootpath, 'vegalite_data', f'vegalite_{file_version}.json')

    if not os.path.exists(file):
        raise FileNotFoundError(f'The vegalite data {file} does not exist.')

    with open(file, 'r') as f:
        spec = json.load(f)

    if version is None or '$schema' in spec:
        return spec

    # Sample versions that might show up
    schema_version = {
        2: 'v2.6.0',
        3: 'v3.6.0',
        4: 'v4.6.0',
        5: 'v5.1.0'
    }[version]
    spec['$schema'] = f'https://vega.github.io/schema/vega-lite/{schema_version}.json'

    return spec


@pytest.mark.parametrize(
    'version',
    [1, 2, 3, 4, 5, None]
)
def test_vegalite_major_version(vegalite_spec, version):
    vegalite = folium.features.VegaLite(vegalite_spec)

    if version is None:
        assert vegalite.vegalite_major_version is None
    else:
        assert vegalite.vegalite_major_version == version

# GeoJsonTooltip GeometryCollection
def test_geojson_tooltip():
    m = folium.Map([30.5, -97.5], zoom_start=10)
    folium.GeoJson(os.path.join(rootpath, 'kuntarajat.geojson'),
                   tooltip=folium.GeoJsonTooltip(fields=['code', 'name'])
                   ).add_to(m)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        m._repr_html_()
        assert issubclass(w[-1].category, UserWarning), 'GeoJsonTooltip GeometryCollection test failed.'


# GeoJsonMarker type validation.
def test_geojson_marker():
    m = folium.Map([30.4, -97.5], zoom_start=10)
    with pytest.raises(TypeError):
        folium.GeoJson(
                os.path.join(rootpath, 'subwaystations.geojson'),
                marker=ClickForMarker()
            ).add_to(m)


def test_geojson_find_identifier():

    def _create(*properties):
        return {"type": "FeatureCollection", "features": [
            {"type": "Feature", "properties": item}
            for item in properties]}

    def _assert_id_got_added(data):
        _geojson = GeoJson(data)
        assert _geojson.find_identifier() == 'feature.id'
        assert _geojson.data['features'][0]['id'] == '0'

    data_with_id = _create(None, None)
    data_with_id['features'][0]['id'] = 'this-is-an-id'
    data_with_id['features'][1]['id'] = 'this-is-another-id'
    geojson = GeoJson(data_with_id)
    assert geojson.find_identifier() == 'feature.id'
    assert geojson.data['features'][0]['id'] == 'this-is-an-id'

    data_with_unique_properties = _create(
        {'property-key': 'some-value'},
        {'property-key': 'another-value'},
    )
    geojson = GeoJson(data_with_unique_properties)
    assert geojson.find_identifier() == 'feature.properties.property-key'

    data_with_unique_properties = _create(
        {'property-key': 42},
        {'property-key': 43},
        {'property-key': 'or a string'},
    )
    geojson = GeoJson(data_with_unique_properties)
    assert geojson.find_identifier() == 'feature.properties.property-key'

    # The test cases below have no id field or unique property,
    # so an id will be added to the data.

    data_with_identical_ids = _create(None, None)
    data_with_identical_ids['features'][0]['id'] = 'identical-ids'
    data_with_identical_ids['features'][1]['id'] = 'identical-ids'
    _assert_id_got_added(data_with_identical_ids)

    data_with_some_missing_ids = _create(None, None)
    data_with_some_missing_ids['features'][0]['id'] = 'this-is-an-id'
    # the second feature doesn't have an id
    _assert_id_got_added(data_with_some_missing_ids)

    data_with_identical_properties = _create(
        {'property-key': 'identical-value'},
        {'property-key': 'identical-value'},
    )
    _assert_id_got_added(data_with_identical_properties)

    data_bare = _create(None)
    _assert_id_got_added(data_bare)

    data_empty_dict = _create({})
    _assert_id_got_added(data_empty_dict)

    data_without_properties = _create(None)
    del data_without_properties['features'][0]['properties']
    _assert_id_got_added(data_without_properties)

    data_some_without_properties = _create({'key': 'value'}, 'will be deleted')
    # the first feature has properties, but the second doesn't
    del data_some_without_properties['features'][1]['properties']
    _assert_id_got_added(data_some_without_properties)

    data_with_nested_properties = _create({
        "summary": {"distance": 343.2},
        "way_points": [3, 5],
    })
    _assert_id_got_added(data_with_nested_properties)

    data_with_incompatible_properties = _create({
        "summary": {"distances": [0, 6], "durations": None},
        "way_points": [3, 5],
    })
    _assert_id_got_added(data_with_incompatible_properties)

    data_loose_geometry = {"type": "LineString", "coordinates": [
        [3.961389, 43.583333], [3.968056, 43.580833], [3.974722, 43.578333],
        [3.986389, 43.575278], [3.998333, 43.5725], [4.163333, 43.530556],
    ]}
    geojson = GeoJson(data_loose_geometry)
    geojson.convert_to_feature_collection()
    assert geojson.find_identifier() == 'feature.id'
    assert geojson.data['features'][0]['id'] == '0'


def test_geometry_collection_get_bounds():
    """Assert #1599 is fixed"""
    geojson_data = {
        "geometries": [
            {
                "coordinates": [
                    [
                        [-1, 1],
                        [0, 2],
                        [-3, 4],
                        [2, 0],
                    ]
                ],
                "type": "Polygon",
            },
        ],
        "type": "GeometryCollection",
    }
    assert folium.GeoJson(geojson_data).get_bounds() == [[0, -3], [4, 2]]
