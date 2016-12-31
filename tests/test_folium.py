# -*- coding: utf-8 -*-

"""
Folium Tests
-------

"""
import pytest

import os
import json
try:
    from unittest import mock
except ImportError:
    import mock

import pandas as pd
import jinja2
from jinja2 import Environment, PackageLoader

from six import PY3
import branca.element

import folium
from folium.map import Popup, Marker, FitBounds, FeatureGroup
from folium.features import TopoJson, RectangleMarker, PolygonMarker

rootpath = os.path.abspath(os.path.dirname(__file__))


def setup_data():
    """Import economic data for testing."""
    with open(os.path.join(rootpath, 'us-counties.json'), 'r') as f:
        get_id = json.load(f)

    county_codes = [x['id'] for x in get_id['features']]
    county_df = pd.DataFrame({'FIPS_Code': county_codes}, dtype=str)

    # Read into Dataframe, cast to string for consistency.
    df = pd.read_csv(os.path.join(rootpath, 'us_county_data.csv'),
                     na_values=[' '])
    df['FIPS_Code'] = df['FIPS_Code'].astype(str)

    # Perform an inner join, pad NA's with data from nearest county.
    merged = pd.merge(df, county_df, on='FIPS_Code', how='inner')
    return merged.fillna(method='pad')


def test_get_templates():
    """Test template getting."""

    env = branca.utilities.get_templates()
    assert isinstance(env, jinja2.environment.Environment)


class TestFolium(object):
    """Test class for the Folium library."""

    def setup(self):
        """Setup Folium Map."""
        with mock.patch('branca.element.uuid4') as uuid4:
            uuid4().hex = '0' * 32
            self.map = folium.Map(location=[45.5236, -122.6750], width=900,
                                  height=400, max_zoom=20, zoom_start=4)
        self.env = Environment(loader=PackageLoader('folium', 'templates'))

    def test_init(self):
        """Test map initialization."""

        assert self.map.get_name() == 'map_00000000000000000000000000000000'
        assert self.map.get_root() == self.map._parent
        assert self.map.location == [45.5236, -122.6750]
        assert self.map.zoom_start == 4
        assert self.map.max_lat == 90
        assert self.map.min_lat == -90
        assert self.map.max_lon == 180
        assert self.map.min_lon == -180
        assert self.map.position == 'relative'
        assert self.map.height == (400, 'px')
        assert self.map.width == (900, 'px')
        assert self.map.left == (0, '%')
        assert self.map.top == (0, '%')
        assert self.map.global_switches.prefer_canvas is False
        assert self.map.global_switches.no_touch is False
        assert self.map.global_switches.disable_3d is False
        assert self.map.to_dict() == {
            "name": "Map",
            "id": "00000000000000000000000000000000",
            "children": {
                "openstreetmap": {
                    "name": "TileLayer",
                    "id": "00000000000000000000000000000000",
                    "children": {}
                    }
                }
            }

    def test_cloudmade(self):
        """Test cloudmade tiles and the API key."""
        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles='cloudmade')

        map = folium.Map(location=[45.5236, -122.6750], tiles='cloudmade',
                         API_key='###')
        cloudmade = 'http://{s}.tile.cloudmade.com/###/997/256/{z}/{x}/{y}.png'
        assert map._children['cloudmade'].tiles == cloudmade

        bounds = map.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_builtin_tile(self):
        """Test custom maptiles."""

        default_tiles = ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner']
        for tiles in default_tiles:
            map = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = ''.join(tiles.lower().strip().split())
            url = 'tiles/{}/tiles.txt'.format
            attr = 'tiles/{}/attr.txt'.format
            url = map._env.get_template(url(tiles)).render()
            attr = map._env.get_template(attr(tiles)).render()

            assert map._children[tiles].tiles == url
            assert map._children[tiles].attr == attr

        bounds = map.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_tile(self):
        """Test custom tile URLs."""

        url = 'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
        attr = 'Attribution for custom tiles'

        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles=url)

        map = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert map._children[url].tiles == url
        assert map._children[url].attr == attr

        bounds = map.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_feature_group(self):
        """Test FeatureGroup."""

        map = folium.Map()
        feature_group = FeatureGroup()
        feature_group.add_child(Marker([45, -30], popup=Popup('-30')))
        feature_group.add_child(Marker([45, 30], popup=Popup('30')))
        map.add_child(feature_group)
        map.add_child(folium.map.LayerControl())

        map._repr_html_()

        bounds = map.get_bounds()
        assert bounds == [[45, -30], [45, 30]], bounds

    def test_circle_marker(self):
        """Test circle marker additions."""

        self.map = folium.Map(location=[45.60, -122.8])
        circ_templ = self.env.get_template('circle_marker.js')

        # Single Circle marker.
        marker = folium.features.CircleMarker([45.60, -122.8], popup='Hi')
        self.map.add_child(marker)
        circle_1 = circ_templ.render({'circle': marker.get_name(),
                                      'lat': 45.60,
                                      'lon': -122.8, 'radius': 500,
                                      'weight': 2,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert (''.join(circle_1.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        # Second circle marker.
        marker = folium.features.CircleMarker([45.70, -122.9], popup='Hi', weight=1)
        self.map.add_child(marker)
        circle_2 = circ_templ.render({'circle': marker.get_name(),
                                      'lat': 45.70,
                                      'lon': -122.9, 'radius': 500,
                                      'weight': 1,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert (''.join(circle_2.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        bounds = self.map.get_bounds()
        assert bounds == [[45.6, -122.9], [45.7, -122.8]], bounds

    def test_rectangle_marker(self):
        """Test rectangle marker additions."""

        self.map = folium.Map(location=[45.60, -122.8])
        rect_templ = self.env.get_template('rectangle_marker.js')

        # Single Rectangle marker.
        bounds = [45.60, -122.8, 45.61, -122.7]
        self.map.add_child(RectangleMarker(bounds=bounds, popup='Hi'))
        marker = list(self.map._children.values())[-1]
        rect_1 = rect_templ.render({'RectangleMarker': marker.get_name(),
                                    'location': [45.60, -122.8, 45.61, -122.7],
                                    'color': 'black',
                                    'fill_color': 'black',
                                    'fill_opacity': 0.6,
                                    'weight': 1})
        assert (''.join(rect_1.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        # Second Rectangle marker.
        bounds = [45.70, -122.9, 45.75, -122.5]
        self.map.add_child(RectangleMarker(bounds=bounds, popup='Hi'))
        marker = list(self.map._children.values())[-1]
        rect_2 = rect_templ.render({'RectangleMarker': marker.get_name(),
                                    'location': [45.70, -122.9, 45.75, -122.5],
                                    'color': 'black',
                                    'fill_color': 'black',
                                    'fill_opacity': 0.6,
                                    'weight': 1})
        assert (''.join(rect_2.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        bounds = self.map.get_bounds()
        assert bounds == [[45.6, -122.9], [45.7, -122.8]], bounds

    def test_polygon_marker(self):
        """Test polygon additions."""

        self.map = folium.Map(location=[45.60, -122.8])
        polygon_templ = self.env.get_template('polygon.js')

        # Single PolygonMarker.
        locations = [[35.6636, 139.7634],
                     [35.6629, 139.7664],
                     [35.6663, 139.7706],
                     [35.6725, 139.7632],
                     [35.6728, 139.7627],
                     [35.6720, 139.7606],
                     [35.6682, 139.7588],
                     [35.6663, 139.7627]]
        self.map.add_child(PolygonMarker(locations=locations, popup='Hi'))
        marker = list(self.map._children.values())[-1]
        polygon_1 = polygon_templ.render({'PolygonMarker': marker.get_name(),
                                          'location': locations,
                                          'color': 'black',
                                          'fill_color': 'black',
                                          'fill_opacity': 0.6,
                                          'weight': 1})
        assert (''.join(polygon_1.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        # Second PolygonMarker.
        locations = [[35.5636, 138.7634],
                     [35.5629, 138.7664],
                     [35.5663, 138.7706],
                     [35.5725, 138.7632],
                     [35.5728, 138.7627],
                     [35.5720, 138.7606],
                     [35.5682, 138.7588],
                     [35.5663, 138.7627]]
        self.map.add_child(PolygonMarker(locations=locations, color='red',
                                         fill_color='red', fill_opacity=0.7,
                                         weight=3, popup='Hi'))
        marker = list(self.map._children.values())[-1]
        polygon_2 = polygon_templ.render({'PolygonMarker': marker.get_name(),
                                          'location': locations,
                                          'color': 'red',
                                          'fill_color': 'red',
                                          'fill_opacity': 0.7,
                                          'weight': 3})
        assert (''.join(polygon_2.split())[:-1] in
                ''.join(self.map.get_root().render().split()))

        bounds = self.map.get_bounds()
        assert bounds == [[[35.5636, 138.7634], [35.5629, 138.7664]],
                          [[35.6636, 139.7634], [35.6629, 139.7664]]], bounds

    def test_topo_json_smooth_factor(self):
        """Test topojson smooth factor method."""
        self.map = folium.Map([43, -100], zoom_start=4)

        # Adding TopoJSON as additional layer.
        path = os.path.join(rootpath, 'or_counties_topo.json')
        self.map.choropleth(geo_path=path,
                            topojson='objects.or_counties_geo',
                            smooth_factor=0.5)

        out = self.map._parent.render()

        # Verify TopoJson
        topo_json = [val for key, val in self.map._children.items()
                     if isinstance(val, TopoJson)][0]
        topojson_str = topo_json._template.module.script(topo_json)
        assert ''.join(topojson_str.split())[:-1] in ''.join(out.split())

    def test_map_build(self):
        """Test map build."""

        # Standard map.
        self.setup()
        out = self.map._parent.render()
        html_templ = self.env.get_template('fol_template.html')
        attr = ('Data by <a href="http://openstreetmap.org">OpenStreetMap'
                '</a>,under '
                '<a href="http://www.openstreetmap.org/copyright">ODbL</a>.')
        tile_layers = [
            {'id': 'tile_layer_'+'0'*32,
             'address': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
             'attr': attr,
             'max_zoom': 20,
             'min_zoom': 1,
             'detect_retina': False,
             'no_wrap': False,
             'continuous_world': False
             }]
        tmpl = {'map_id': 'map_' + '0' * 32,
                'lat': 45.5236, 'lon': -122.675,
                'size': 'width: 900.0px; height: 400.0px;',
                'zoom_level': 4,
                'min_lat': -90,
                'max_lat': 90,
                'min_lon': -180,
                'max_lon': 180,
                'tile_layers': tile_layers,
                'crs': 'EPSG3857',
                'world_copy_jump': False
                }
        HTML = html_templ.render(tmpl, plugins={})

        assert ''.join(out.split()) == ''.join(HTML.split())

    def test_tile_attr_unicode(self):
        """Test tile attribution unicode

        Test not cover b'юникод'
        because for python 3 bytes can only contain ASCII literal characters.
        """

        if not PY3:
            map = folium.Map(location=[45.5236, -122.6750],
                             tiles='test', attr=b'unicode')
            map._parent.render()
        else:
            map = folium.Map(location=[45.5236, -122.6750],
                             tiles='test', attr=u'юникод')
            map._parent.render()
        map = folium.Map(location=[45.5236, -122.6750],
                         tiles='test', attr='юникод')
        map._parent.render()

    def test_fit_bounds(self):
        """Test fit_bounds."""
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))

        self.setup()
        self.map.fit_bounds(bounds)
        fitbounds = [val for key, val in self.map._children.items() if
                     isinstance(val, FitBounds)][0]
        out = self.map._parent.render()

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'this': fitbounds,
            'fit_bounds_options': {}, })

        assert ''.join(fit_bounds_rendered.split()) in ''.join(out.split())

        self.setup()
        self.map.fit_bounds(bounds, max_zoom=15, padding=(3, 3))
        fitbounds = [val for key, val in self.map._children.items() if
                     isinstance(val, FitBounds)][0]
        out = self.map._parent.render()

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'fit_bounds_options': json.dumps({'maxZoom': 15,
                                              'padding': (3, 3), },
                                             sort_keys=True),
            'this': fitbounds,
            })

        assert ''.join(fit_bounds_rendered.split()) in ''.join(out.split())

        bounds = self.map.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_icon(self):
        """Test CustomIcon."""
        self.setup()

        icon_image = "http://leafletjs.com/docs/images/leaf-green.png"
        shadow_image = "http://leafletjs.com/docs/images/leaf-shadow.png"

        self.map = folium.Map([45, -100], zoom_start=4)
        i = folium.features.CustomIcon(icon_image,
                                       icon_size=(38, 95),
                                       icon_anchor=(22, 94),
                                       shadow_image=shadow_image,
                                       shadow_size=(50, 64),
                                       shadow_anchor=(4, 62),
                                       popup_anchor=(-3, -76),)
        mk = folium.map.Marker([45, -100], icon=i,
                               popup=folium.map.Popup('Hello'))
        self.map.add_child(mk)
        self.map._parent.render()

        bounds = self.map.get_bounds()
        assert bounds == [[45, -100], [45, -100]], bounds

    def test_tile_layer(self):
        mapa = folium.Map([48., 5.], tiles='stamentoner', zoom_start=6)
        layer = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        mapa.add_child(folium.map.TileLayer(layer, name='OpenStreetMap',
                                            attr='attribution'))
        mapa.add_child(folium.map.TileLayer(layer,
                                            name='OpenStreetMap2',
                                            attr='attribution2',
                                            overlay=True))
        mapa.add_child(folium.map.LayerControl())
        mapa._repr_html_()

        bounds = self.map.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_global_switches(self):
        mapa = folium.Map(prefer_canvas=True)
        assert (mapa.global_switches.prefer_canvas is True and
                mapa.global_switches.no_touch is False and
                mapa.global_switches.disable_3d is False)

        mapb = folium.Map(no_touch=True)
        assert (mapb.global_switches.prefer_canvas is False and
                mapb.global_switches.no_touch is True and
                mapb.global_switches.disable_3d is False)

        mapc = folium.Map(disable_3d=True)
        assert (mapc.global_switches.prefer_canvas is False and
                mapc.global_switches.no_touch is False and
                mapc.global_switches.disable_3d is True)

        mapd = folium.Map(prefer_canvas=True, no_touch=True, disable_3d=True)
        assert (mapd.global_switches.prefer_canvas is True and
                mapd.global_switches.no_touch is True and
                mapd.global_switches.disable_3d is True)
