# -*- coding: utf-8 -*-

"""
Folium Tests
-------

"""

import json
import os

import branca.element

import folium
from folium.features import GeoJson, Choropleth

import jinja2
from jinja2 import Environment, PackageLoader
from jinja2.utils import htmlsafe_json_dumps

import numpy as np
import pandas as pd

import pytest

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


def test_location_args():
    """Test some data types for a location arg."""
    location = np.array([45.5236, -122.6750])
    m = folium.Map(location)
    assert m.location == [45.5236, -122.6750]

    df = pd.DataFrame({"location": [45.5236, -122.6750]})
    m = folium.Map(df["location"])
    assert m.location == [45.5236, -122.6750]


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
        assert self.m.options['zoom'] == 4
        assert self.m.options['maxBounds'] == [[-90, -180], [90, 180]]
        assert self.m.position == 'relative'
        assert self.m.height == (400, 'px')
        assert self.m.width == (900, 'px')
        assert self.m.left == (0, '%')
        assert self.m.top == (0, '%')
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

    def test_builtin_tile(self):
        """Test custom maptiles."""

        default_tiles = [
            "OpenStreetMap",
            "Stamen Terrain",
            "Stamen Toner",
            "CartoDB positron",
            "CartoDB dark_matter",
        ]
        for tiles in default_tiles:
            m = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = "".join(tiles.lower().strip().split())
            url = "tiles/{}/tiles.txt".format
            attr = "tiles/{}/attr.txt".format
            url = m._env.get_template(url(tiles)).render()
            attr = m._env.get_template(attr(tiles)).render()

            assert m._children[tiles].tiles == url
            assert htmlsafe_json_dumps(attr) in m._parent.render()

        bounds = m.get_bounds()
        assert bounds == [[None, None], [None, None]], bounds

    def test_custom_tile(self):
        """Test custom tile URLs."""

        url = "http://{s}.custom_tiles.org/{z}/{x}/{y}.png"
        attr = "Attribution for custom tiles"

        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles=url)

        m = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert m._children[url].tiles == url
        assert attr in m._parent.render()

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

    def test_choropleth_key_on(self):
        """Test to make sure that Choropleth function doesn't raises
        a ValueError when the 'key_on' field is set to a column that might
        have 0 as a value.
        """
        with open(os.path.join(rootpath, 'geo_grid.json')) as f:
            geo_data = json.load(f)
        data = pd.DataFrame({'idx': {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5},
                             'value': {'0': 78.0, '1': 39.0, '2': 0.0, '3': 81.0, '4': 42.0, '5': 68.0}})
        fill_color = 'BuPu'
        columns = ['idx', 'value']
        key_on = 'feature.properties.idx'

        Choropleth(
            geo_data=geo_data,
            data=data,
            key_on=key_on,
            fill_color=fill_color,
            columns=columns)

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
        """Test tile attribution unicode"""
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
        out = m._parent.render()
        out_str = ''.join(out.split())
        assert "preferCanvas:true" in out_str
        assert not m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(no_touch=True)
        out = m._parent.render()
        out_str = ''.join(out.split())
        assert "preferCanvas:false" in out_str
        assert m.global_switches.no_touch
        assert not m.global_switches.disable_3d

        m = folium.Map(disable_3d=True)
        out = m._parent.render()
        out_str = ''.join(out.split())
        assert "preferCanvas:false" in out_str
        assert not m.global_switches.no_touch
        assert m.global_switches.disable_3d

        m = folium.Map(prefer_canvas=True, no_touch=True, disable_3d=True)
        out = m._parent.render()
        out_str = ''.join(out.split())
        assert "preferCanvas:true" in out_str
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
