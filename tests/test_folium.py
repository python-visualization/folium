# -*- coding: utf-8 -*-

"""
Folium Tests
-------

"""

from __future__ import (absolute_import, division, print_function)

import json
import os

import branca.element

import folium
from folium.features import GeoJson, Choropleth

import jinja2
from jinja2 import Environment, PackageLoader

import pandas as pd

import pytest

from six import PY3

try:
    from unittest import mock
except ImportError:
    import mock


rootpath = os.path.abspath(os.path.dirname(__file__))

# For testing remote requests
remote_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'  # noqa


def setup_data():
    """Import economic data for testing."""
    with open(os.path.join(rootpath, 'us-counties.json')) as f:
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
            attr = 'http://openstreetmap.org'
            self.m = folium.Map(
                location=[45.5236, -122.6750],
                width=900,
                height=400,
                max_zoom=20,
                zoom_start=4,
                max_bounds=True,
                attr=attr
            )
        self.env = Environment(loader=PackageLoader('folium', 'templates'))

    def test_init(self):
        """Test map initialization."""

        assert self.m.get_name() == 'map_00000000000000000000000000000000'
        assert self.m.get_root() == self.m._parent
        assert self.m.location == [45.5236, -122.6750]
        assert self.m.zoom_start == 4
        assert self.m.max_lat == 90
        assert self.m.min_lat == -90
        assert self.m.max_lon == 180
        assert self.m.min_lon == -180
        assert self.m.position == 'relative'
        assert self.m.height == (400, 'px')
        assert self.m.width == (900, 'px')
        assert self.m.left == (0, '%')
        assert self.m.top == (0, '%')
        assert self.m.global_switches.prefer_canvas is False
        assert self.m.global_switches.no_touch is False
        assert self.m.global_switches.disable_3d is False
        assert self.m.to_dict() == {
            'name': 'Map',
            'id': '00000000000000000000000000000000',
            'children': {
                'openstreetmap': {
                    'name': 'TileLayer',
                    'id': '00000000000000000000000000000000',
                    'children': {}
                    }
                }
            }

    def test_cloudmade(self):
        """Test cloudmade tiles and the API key."""
        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles='cloudmade')

        m = folium.Map(location=[45.5236, -122.6750], tiles='cloudmade',
                       API_key='###')
        cloudmade = 'http://{s}.tile.cloudmade.com/###/997/256/{z}/{x}/{y}.png'
        assert m._children['cloudmade'].tiles == cloudmade

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_builtin_tile(self):
        """Test custom maptiles."""

        default_tiles = ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner']
        for tiles in default_tiles:
            m = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = ''.join(tiles.lower().strip().split())
            url = 'tiles/{}/tiles.txt'.format
            attr = 'tiles/{}/attr.txt'.format
            url = m._env.get_template(url(tiles)).render()
            attr = m._env.get_template(attr(tiles)).render()

            assert m._children[tiles].tiles == url
            assert m._children[tiles].attr == attr

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_tile(self):
        """Test custom tile URLs."""

        url = 'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
        attr = 'Attribution for custom tiles'

        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles=url)

        m = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert m._children[url].tiles == url
        assert m._children[url].attr == attr

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_feature_group(self):
        """Test FeatureGroup."""

        m = folium.Map()
        feature_group = folium.FeatureGroup()
        feature_group.add_child(folium.Marker([45, -30],
                                              popup=folium.Popup('-30')))
        feature_group.add_child(folium.Marker([45, 30],
                                              popup=folium.Popup('30')))
        m.add_child(feature_group)
        m.add_child(folium.LayerControl())

        m._repr_html_()

        bounds = m.get_bounds()
        assert bounds == [[45, -30], [45, 30]], bounds

    def test_topo_json_smooth_factor(self):
        """Test topojson smooth factor method."""
        self.m = folium.Map([43, -100], zoom_start=4)

        # Adding TopoJSON as additional layer.
        with open(os.path.join(rootpath, 'or_counties_topo.json')) as f:
            choropleth = Choropleth(f, topojson='objects.or_counties_geo',
                                    smooth_factor=0.5).add_to(self.m)

        out = self.m._parent.render()

        # Verify TopoJson
        topo_json = choropleth.geojson
        topojson_str = topo_json._template.module.script(topo_json)
        assert ''.join(topojson_str.split())[:-1] in ''.join(out.split())

    def test_map_build(self):
        """Test map build."""

        # Standard map.
        self.setup()
        rendered = [line.strip() for line in self.m._parent.render().splitlines() if line.strip()]

        html_templ = self.env.get_template('fol_template.html')
        attr = 'http://openstreetmap.org'
        tile_layers = [
            {'id': 'tile_layer_'+'0'*32,
             'address': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
             'attr': attr,
             'max_native_zoom': 20,
             'max_zoom': 20,
             'min_zoom': 0,
             'detect_retina': False,
             'no_wrap': False,
             'tms': False,
             'opacity': 1,
             'subdomains': 'abc'
             }]
        tmpl = {'map_id': 'map_' + '0' * 32,
                'lat': 45.5236, 'lon': -122.675,
                'width': 'width: 900.0px;',
                'height': 'height: 400.0px;',
                'zoom_level': 4,
                'max_bounds': True,
                'min_lat': -90,
                'max_lat': 90,
                'min_lon': -180,
                'max_lon': 180,
                'tile_layers': tile_layers,
                'crs': 'EPSG3857',
                'world_copy_jump': False,
                'zoom_control': True
                }
        HTML = html_templ.render(tmpl, plugins={})
        expected = [line.strip() for line in HTML.splitlines() if line.strip()]

        assert rendered == expected

    def test_choropleth_features(self):
        """Test to make sure that Choropleth function doesn't allow
        values outside of the domain defined by bins.

        It also tests that all parameters work as expected regarding
        nan and missing values.
        """
        self.setup()

        with open(os.path.join(rootpath, 'us-counties.json')) as f:
            geo_data = json.load(f)
        data = {'1001': -1}
        fill_color = 'BuPu'
        key_on = 'id'

        with pytest.raises(ValueError):
            Choropleth(
                geo_data=geo_data,
                data=data,
                key_on=key_on,
                fill_color=fill_color,
                bins=[0, 1, 2, 3]).add_to(self.m)
            self.m._parent.render()

        Choropleth(
            geo_data=geo_data,
            data={'1001': 1, '1003': float('nan')},
            key_on=key_on,
            fill_color=fill_color,
            fill_opacity=0.543212345,
            nan_fill_color='a_random_color',
            nan_fill_opacity=0.123454321).add_to(self.m)

        out = self.m._parent.render()
        out_str = ''.join(out.split())
        assert '"fillColor":"a_random_color","fillOpacity":0.123454321' in out_str
        assert '"fillOpacity":0.543212345' in out_str

    def test_choropleth_warning(self):
        """Test that the Map.choropleth method works and raises a warning."""
        self.setup()
        with open(os.path.join(rootpath, 'us-counties.json')) as f:
            geo_data = json.load(f)
        with pytest.warns(FutureWarning):
            self.m.choropleth(geo_data)
        assert any([isinstance(child, Choropleth)
                    for child in self.m._children.values()])

    def test_tile_attr_unicode(self):
        """Test tile attribution unicode

        Test does not cover b'юникод'
        because for python 3 bytes can only contain ASCII literal characters.
        """

        if not PY3:
            m = folium.Map(location=[45.5236, -122.6750],
                           tiles='test', attr=b'unicode')
            m._parent.render()
        else:
            m = folium.Map(location=[45.5236, -122.6750],
                           tiles='test', attr=u'юникод')
            m._parent.render()
        m = folium.Map(location=[45.5236, -122.6750],
                       tiles='test', attr='юникод')
        m._parent.render()

    def test_fit_bounds(self):
        """Test fit_bounds."""
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))

        self.setup()
        self.m.fit_bounds(bounds)
        fitbounds = [val for key, val in self.m._children.items() if
                     isinstance(val, folium.FitBounds)][0]
        out = self.m._parent.render()

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'this': fitbounds,
            'fit_bounds_options': {}, })

        assert ''.join(fit_bounds_rendered.split()) in ''.join(out.split())

        self.setup()
        self.m.fit_bounds(bounds, max_zoom=15, padding=(3, 3))
        fitbounds = [val for key, val in self.m._children.items() if
                     isinstance(val, folium.FitBounds)][0]
        out = self.m._parent.render()

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'fit_bounds_options': json.dumps({'maxZoom': 15,
                                              'padding': (3, 3), },
                                             sort_keys=True),
            'this': fitbounds,
            })

        assert ''.join(fit_bounds_rendered.split()) in ''.join(out.split())

        bounds = self.m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_icon(self):
        """Test CustomIcon."""
        self.setup()

        icon_image = 'http://leafletjs.com/docs/images/leaf-green.png'
        shadow_image = 'http://leafletjs.com/docs/images/leaf-shadow.png'

        self.m = folium.Map([45, -100], zoom_start=4)
        i = folium.features.CustomIcon(icon_image,
                                       icon_size=(38, 95),
                                       icon_anchor=(22, 94),
                                       shadow_image=shadow_image,
                                       shadow_size=(50, 64),
                                       shadow_anchor=(4, 62),
                                       popup_anchor=(-3, -76),)
        mk = folium.Marker([45, -100], icon=i,
                           popup=folium.Popup('Hello'))
        self.m.add_child(mk)
        self.m._parent.render()

        bounds = self.m.get_bounds()
        assert bounds == [[45, -100], [45, -100]], bounds

    def test_global_switches(self):
        m = folium.Map(prefer_canvas=True)
        assert m.global_switches.prefer_canvas
        assert not m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(no_touch=True)
        assert not m.global_switches.prefer_canvas
        assert m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(disable_3d=True)
        assert not m.global_switches.prefer_canvas
        assert not m.global_switches.no_touch
        assert m.global_switches.disable_3d

        m = folium.Map(prefer_canvas=True, no_touch=True, disable_3d=True)
        assert m.global_switches.prefer_canvas
        assert m.global_switches.no_touch
        assert m.global_switches.disable_3d

    @pytest.mark.web
    def test_json_request(self):
        """Test requests for remote GeoJSON files."""
        self.m = folium.Map(zoom_start=4)

        # Adding remote GeoJSON as additional layer.
        GeoJson(remote_url, smooth_factor=0.5).add_to(self.m)

        self.m._parent.render()
        bounds = self.m.get_bounds()
        assert bounds == [[18.948267, -178.123152], [71.351633, 173.304726]], bounds  # noqa
