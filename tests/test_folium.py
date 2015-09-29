# -*- coding: utf-8 -*-

"""
Folium Tests
-------

"""
import pytest

import os
import json
import mock
import pandas as pd
import jinja2
from jinja2 import Environment, PackageLoader
import vincent
import folium
from folium.six import PY3
from folium.plugins import ScrollZoomToggler, MarkerCluster
from folium.element import Html
from folium.map import Popup, Marker, Icon
from folium.features import DivIcon, CircleMarker, LatLngPopup, GeoJson,\
    GeoJsonStyle, ColorScale, TopoJson


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

    env = folium.utilities.get_templates()
    assert isinstance(env, jinja2.environment.Environment) == True


class TestFolium(object):
    """Test class for the Folium library."""

    def setup(self):
        """Setup Folium Map."""
        with mock.patch('folium.element.uuid4') as uuid4:
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
        assert map._children['cloudmade'].tiles == ('http://{s}.tile.cloudmade.com'
                                              '/###/997/256/{z}/{x}/{y}.png')

    def test_builtin_tile(self):
        """Test custom maptiles."""

        default_tiles = ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner']
        for tiles in default_tiles:
            map = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = ''.join(tiles.lower().strip().split())
            url = map._env.get_template('tiles/{}/tiles.txt'.format(tiles)).render()
            attr = map._env.get_template('tiles/{}/attr.txt'.format(tiles)).render()

            assert map._children[tiles].tiles == url
            assert map._children[tiles].attr == attr

    def test_custom_tile(self):
        """Test custom tile URLs."""

        url = 'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
        attr = 'Attribution for custom tiles'

        with pytest.raises(ValueError):
            folium.Map(location=[45.5236, -122.6750], tiles=url)

        map = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert map._children[url].tiles == url
        assert map._children[url].attr == attr

    def test_wms_layer(self):
        """Test WMS layer URLs."""

        map = folium.Map(location=[44, -73], zoom_start=3)
        wms_url = 'http://gis.srh.noaa.gov/arcgis/services/NDFDTemps/'
        wms_url += 'MapServer/WMSServer'
        wms_name = "Temperature"
        wms_layers = 16
        wms_format = "image/png"
        map.add_wms_layer(wms_name=wms_name,
                          wms_url=wms_url,
                          wms_format=wms_format,
                          wms_layers=wms_layers,
                          wms_transparent=True)

        wms_temp = self.env.get_template('wms_layer.js')
        wms = wms_temp.render({'wms_name': map._children[wms_name].get_name(),
                               'wms_url': wms_url,
                               'wms_format': wms_format,
                               'wms_layer_names': wms_layers,
                               'wms_transparent': 'true'})
        assert ''.join(wms.split())[:-1] in ''.join(map.get_root().render().split())

    def test_simple_marker(self):
        """Test simple marker addition."""

        self.map = folium.Map(location=[44, -73], zoom_start=3)
        mark_templ = self.env.get_template('simple_marker.js')
        popup_templ = self.env.get_template('simple_popup.js')

        # Single Simple marker.
        self.map.simple_marker(location=[45.50, -122.7])
        marker_1 = list(self.map._children.values())[-1]
        mark_1 = mark_templ.render({'marker': marker_1.get_name(),
                                    'lat': 45.50,
                                    'lon': -122.7,
                                    'icon': "{icon:new L.Icon.Default()}"})
        assert ''.join(mark_1.split())[:-1] in ''.join(self.map.get_root().render().split())
        #assert self.map.template_vars['custom_markers'][0][2] == ""

        # Test Simple marker addition.
        self.map.simple_marker(location=[45.60, -122.8], popup='Hi')
        marker_2 = list(self.map._children.values())[-1]
        popup_2 = list(marker_2._children.values())[-1]
        html_2 = list(popup_2.html._children.values())[0]
        mark_2 = mark_templ.render({'marker': marker_2.get_name(),
                                    'lat': 45.60,
                                    'lon': -122.8,
                                    'icon': "{icon:new L.Icon.Default()}"})
        pop_2 = popup_templ.render({'pop_name': popup_2.get_name(),
                                    'pop_txt': 'Hi',
                                    'html_name': html_2.get_name(),
                                    'width': 300})
        #assert self.map.mark_cnt['simple'] == 2
        assert ''.join(mark_2.split())[:-1] in ''.join(self.map.get_root().render().split())
        assert ''.join(pop_2.split())[:-1] in ''.join(self.map.get_root().render().split())
        #assert self.map.template_vars['custom_markers'][1][2] == pop_2

        # Test no popup.
        self.map.simple_marker(location=[45.60, -122.8])
        for child in list(self.map._children.values())[-1]._children.values():
            assert not isinstance(child, Popup)

    def test_div_markers(self):
        '''Test div marker list addition'''
        self.map = folium.Map(location=[37.421114, -122.128314])

        icon_templ = self.env.get_template('static_div_icon.js')
        mark_templ = self.env.get_template('simple_marker.js')
        popup_templ = self.env.get_template('simple_popup.js')

        # Test with popups (expected use case).
        locations = [[37.421114, -122.128314],
                     [37.391637, -122.085416],
                     [37.388832, -122.087709]]
        popups = ['1437494575531', '1437492135937', '1437493590434']

        self.map.div_markers(locations=locations, popups=popups)

        markers = [marker for marker in self.map._children.values() if isinstance(marker,Marker)]
        assert len(markers)==3

        for marker, location, pop in zip(markers, locations, popups):
            icon = list(marker._children.values())[0]
            popup = list(marker._children.values())[1]
            html = list(popup.html._children.values())[0]

            assert isinstance(icon,DivIcon)
            assert isinstance(popup,Popup)
            assert isinstance(html,Html)

            icon_1 = icon_templ.render({'icon_name': icon.get_name(),
                                        'size': 10})
            mark_1 = mark_templ.render({'marker': marker.get_name(),
                                        'lat': location[0],
                                        'lon': location[1],
                                        'icon': "{icon:new L.Icon.Default()}"})
            popup_1 = popup_templ.render({'pop_name': popup.get_name(),
                                          'html_name' : html.get_name(),
                                          'pop_txt': '{}'.format(pop),
                                          'width': 300})

            out = ''.join(self.map.get_root().render().split())
            assert ''.join(icon_1.split())[:-1] in out
            assert ''.join(mark_1.split())[:-1] in out
            assert ''.join(popup_1.split())[:-1] in out

        # Test no popup. If there are no popups,
        # then we should get a RuntimeError.
        with pytest.raises(TypeError):
            self.map.div_markers([[45.60, -122.8]])

    def test_circle_marker(self):
        """Test circle marker additions."""

        self.map = folium.Map(location=[45.60, -122.8])
        circ_templ = self.env.get_template('circle_marker.js')

        # Single Circle marker.
        self.map.circle_marker(location=[45.60, -122.8], popup='Hi')
        marker = list(self.map._children.values())[-1]
        circle_1 = circ_templ.render({'circle': marker.get_name(),
                                      'lat': 45.60,
                                      'lon': -122.8, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert ''.join(circle_1.split())[:-1] in ''.join(self.map.get_root().render().split())

        # Second circle marker.
        self.map.circle_marker(location=[45.70, -122.9], popup='Hi')
        marker = list(self.map._children.values())[-1]
        circle_2 = circ_templ.render({'circle': marker.get_name(),
                                      'lat': 45.70,
                                      'lon': -122.9, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert ''.join(circle_2.split())[:-1] in ''.join(self.map.get_root().render().split())

    def test_poly_marker(self):
        """Test polygon marker."""

        self.map = folium.Map(location=[45.5, -122.5])
        poly_temp = self.env.get_template('poly_marker.js')

        self.map.polygon_marker(location=[45.5, -122.5])
        marker = list(self.map._children.values())[-1]
        polygon = poly_temp.render({'marker': marker.get_name(),
                                    'lat': 45.5,
                                    'lon': -122.5,
                                    'line_color': 'black',
                                    'line_opacity': 1,
                                    'line_weight': 2,
                                    'fill_color': 'blue',
                                    'fill_opacity': 1,
                                    'num_sides': 4,
                                    'rotation': 0,
                                    'radius': 15})

        assert (''.join(polygon.split()))[-1] in ''.join(self.map.get_root().render().split())

    def test_latlng_pop(self):
        """Test lat/lon popovers."""

        self.map.lat_lng_popover()
        pop = list(self.map._children.values())[-1]
        pop_templ = self.env.get_template('lat_lng_popover.js').render(popup=pop.get_name(),
                                                                      map=self.map.get_name())
        assert (''.join(pop_templ.split()))[:-1] in ''.join(self.map.get_root().render().split())

    def test_click_for_marker(self):
        """Test click for marker functionality."""

        # Lat/lon popover.
        self.map = folium.Map([46,3])
        self.map.click_for_marker()
        click_templ = self.env.get_template('click_for_marker.js')
        click = click_templ.render({'popup': ('"Latitude: " + lat + "<br>'
                                              'Longitude: " + lng '),
                                   'map' : self.map.get_name()})
        assert (''.join(click.split()))[:-1] in ''.join(self.map.get_root().render().split())

        # Custom popover.
        self.map.click_for_marker(popup='Test')
        click_templ = self.env.get_template('click_for_marker.js')
        click = click_templ.render({'popup': '"Test"',
                                   'map' : self.map.get_name()})
        assert (''.join(click.split()))[:-1] in ''.join(self.map.get_root().render().split())

    def test_vega_popup(self):
        """Test vega popups."""

        self.map = folium.Map([45.60, -122.8])

        vega_templ = self.env.get_template('vega_marker.js')
        vega_parse = self.env.get_template('vega_parse.js')

        vis = vincent.Bar(width=675 - 75, height=350 - 50, no_data=True)
        data = json.loads(vis.to_json())

        self.map.simple_marker(location=[45.60, -122.8],
                               popup=(vis, 'vis.json'))

        marker = list(self.map._children.values())[-1]
        popup = list(marker._children.values())[-1]
        vega = list(popup._children.values())[-1]
        vega_str = vega_templ.render({'vega': vega.get_name(),
                                      'popup':popup.get_name(),
                                      'marker':marker.get_name(),
                                      'vega_json':json.dumps(data),
                                      })
        out = ''.join(self.map.get_root().render().split())
        assert ''.join(vega_parse.render().split()) in out
        assert (''.join(vega_str.split()))[:-1] in out

    def test_geo_json_simple(self):
        """Test geojson method."""

        # No data binding.
        self.map = folium.Map([43, -100], zoom_start=4)
        path = os.path.join(rootpath, 'us-counties.json')
        self.map.geo_json(geo_path=path)

        geo_json = [x for x in self.map._children.values() if isinstance(x,GeoJson)][0]
        color_scale = [x for x in self.map._children.values() if isinstance(x,ColorScale)][0]
        geo_json_style = list(geo_json._children.values())[0]
        out = ''.join(self.map._parent.render().split())

        # Verify the geo_json object
        obj_temp = self.env.get_template('geo_json.js')
        obj = obj_temp.render(this = geo_json)
        assert ''.join(obj.split())[:-1] in out

        # Verify the style
        assert geo_json_style.color == 'black'
        assert geo_json_style.weight == 1
        assert geo_json_style.opacity == 1
        assert geo_json_style.fill_color == 'blue'
        assert geo_json_style.fill_opacity == 0.6
        assert geo_json_style.dash_array == 0
        style = geo_json_style._template.module.script(geo_json_style)
        assert ''.join(style.split())[:-1] in out

        # Verify the color_scale
        colorsc_temp = self.env.get_template('color_scale.js')
        colorsc = colorsc_temp.render(this=color_scale)
        assert ''.join(colorsc.split())[:-1] in out

    def test_geo_json_bad_color(self):
        """Test geojson method."""

        self.map = folium.Map([43, -100], zoom_start=4)

        path = os.path.join(rootpath, 'us-counties.json')

        # Data binding incorrect color value error.
        data = setup_data()
        with pytest.raises(ValueError):
            self.map.geo_json(path, data=data,
                              columns=['FIPS_Code', 'Unemployed_2011'],
                              key_on='feature.id', fill_color='blue')

    def test_geo_json_bad_threshold_scale(self):
        """Test geojson method."""

        self.map = folium.Map([43, -100], zoom_start=4)

        path = os.path.join(rootpath, 'us-counties.json')

        # Data binding threshold_scale too long.
        data = setup_data()
        with pytest.raises(ValueError):
            self.map.geo_json(path, data=data,
                              columns=['FIPS_Code', 'Unemployed_2011'],
                              key_on='feature.id',
                              threshold_scale=[1, 2, 3, 4, 5, 6, 7],
                              fill_color='YlGnBu')

    def test_geo_json_data_binding(self):
        """Test geojson method."""

        data = setup_data()

        self.map = folium.Map([43, -100], zoom_start=4)

        path = os.path.join(rootpath, 'us-counties.json')

        # With DataFrame data binding, default threshold scale.
        self.map.geo_json(geo_path=path, data=data,
                          threshold_scale=[4.0, 1000.0, 3000.0, 5000.0, 9000.0],
                          columns=['FIPS_Code', 'Unemployed_2011'],
                          key_on='feature.id', fill_color='YlGnBu',
                          reset=True)

        out = self.map._parent.render()

        geo_json = [x for x in self.map._children.values() if isinstance(x,GeoJson)][0]
        color_scale = [x for x in self.map._children.values() if isinstance(x,ColorScale)][0]
        geo_json_style = list(geo_json._children.values())[0]

        # Verify the geo_json object
        obj_temp = self.env.get_template('geo_json.js')
        obj = obj_temp.render(this = geo_json)
        assert ''.join(obj.split())[:-1] in ''.join(out.split())

        # Verify the style
        assert geo_json_style.color == 'black'
        assert geo_json_style.weight == 1
        assert geo_json_style.opacity == 1
        assert geo_json_style.fill_color == 'YlGnBu'
        assert geo_json_style.fill_opacity == 0.6
        assert geo_json_style.dash_array == 0
        style = geo_json_style._template.module.script(geo_json_style)
        assert ''.join(style.split())[:-1] in ''.join(out.split())

        # Verify the colorscale
        domain = [4.0, 1000.0, 3000.0, 5000.0, 9000.0]
        palette = folium.utilities.color_brewer('YlGnBu')
        d3range = palette[0: len(domain) + 2]
        colorscale_obj = [val for key,val in self.map._children.items() if isinstance(val, ColorScale)][0]
        colorscale_temp = self.env.get_template('d3_threshold.js')
        colorscale = colorscale_temp.render({
            'this' : colorscale_obj,
            'domain': domain,
            'range': d3range})
        assert ''.join(colorscale.split())[:-1] in ''.join(out.split())

    def test_topo_json(self):
        """Test geojson method."""

        self.map = folium.Map([43, -100], zoom_start=4)

        path = os.path.join(rootpath, 'us-counties.json')

        # Adding TopoJSON as additional layer.
        path_2 = 'or_counties_topo.json'
        self.map.geo_json(geo_path=path_2, topojson='objects.or_counties_geo')

        out = self.map._parent.render()

        # Verify TopoJson
        topo_json = [val for key,val in self.map._children.items()\
                 if isinstance(val,TopoJson)][0]
        topojson_str = topo_json._template.module.script(topo_json)
        assert ''.join(topojson_str.split())[:-1] in ''.join(out.split())

    def test_map_build(self):
        """Test map build."""

        # Standard map.
        self.setup()
        out = self.map._parent.render()
        html_templ = self.env.get_template('fol_template.html')

        tile_layers = [
            {
                'id' : 'tile_layer_'+'0'*32,
                'address' : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attr': ('Map data (c) <a href="http://openstreetmap.org">'
                         'OpenStreetMap</a> contributors'),
                'max_zoom': 20,
                'min_zoom': 1,
                }
            ]
        tmpl = {
                'map_id': 'map_' + '0' * 32,
                'lat': 45.5236, 'lon': -122.675,
                'size': 'width: 900.0px; height: 400.0px;',
                'zoom_level': 4,
                'min_lat': -90,
                'max_lat': 90,
                'min_lon': -180,
                'max_lon': 180,
                'tile_layers': tile_layers,
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

    def test_create_map(self):
        """Test create map."""

        map = folium.Map(location=[45.5236, -122.6750],
                         tiles='test', attr='юникод')

        # Add json data.
        path = os.path.join(rootpath, 'us-counties.json')
        data = setup_data()
        map.geo_json(geo_path=path, data=data,
                     columns=['FIPS_Code', 'Unemployed_2011'],
                     key_on='feature.id', fill_color='YlGnBu',
                     reset=True)

        # Add plugins.
        map.polygon_marker(location=[45.5, -122.5])

        # Test write.
        map._parent.render()

    def test_line(self):
        """Test line."""

        line_temp = self.env.get_template('polyline.js')

        line_opts = {
            'color': 'blue',
            'weight': 2,
            'opacity': 1
        }
        locations = [
            [[45.5236, -122.6750], [45.5236, -122.6751]],
            [[45.5237, -122.6750], [45.5237, -122.6751]],
            [[45.5238, -122.6750], [45.5238, -122.6751]]
        ]
        line_rendered = line_temp.render({'line': 'line_1',
                                          'locations': locations,
                                          'options': line_opts})

        self.map.line(locations=locations,
                      line_color=line_opts['color'],
                      line_weight=line_opts['weight'],
                      line_opacity=line_opts['opacity'])
        assert self.map.template_vars['lines'][0][0] == line_rendered

    def test_multi_polyline(self):
        """Test multi_polyline."""

        multiline_temp = self.env.get_template('multi_polyline.js')

        multiline_opts = {'color': 'blue',
                          'weight': 2,
                          'opacity': 1}
        locations = [[[45.5236, -122.6750], [45.5236, -122.6751]],
                     [[45.5237, -122.6750], [45.5237, -122.6751]],
                     [[45.5238, -122.6750], [45.5238, -122.6751]]]
        multiline_rendered = multiline_temp.render({'multiline': 'multiline_1',
                                                    'locations': locations,
                                                    'options': multiline_opts})

        self.map.multiline(locations=locations,
                           line_color=multiline_opts['color'],
                           line_weight=multiline_opts['weight'],
                           line_opacity=multiline_opts['opacity'])
        assert self.map.template_vars['multilines'][0][0] == multiline_rendered

    def test_fit_bounds(self):
        """Test fit_bounds."""
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))
        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'fit_bounds_options': {}, })

        self.map.fit_bounds(bounds)
        assert self.map.template_vars['fit_bounds'] == fit_bounds_rendered

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
            'bounds': json.dumps(bounds),
            'fit_bounds_options': json.dumps({'maxZoom': 15,
                                              'padding': (3, 3), },
                                             sort_keys=True),
        })

        self.map.fit_bounds(bounds, max_zoom=15, padding=(3, 3))

        assert self.map.template_vars['fit_bounds'] == fit_bounds_rendered

    def test_image_overlay(self):
        """Test image overlay."""
        from numpy.random import random
        from folium.utilities import write_png
        import base64

        data = random((100, 100))
        png_str = write_png(data)
        with open('data.png', 'wb') as f:
            f.write(png_str)
        png = "data:image/png;base64,{}".format
        inline_image_url = png(base64.b64encode(png_str).decode('utf-8'))

        image_tpl = self.env.get_template('image_layer.js')
        image_name = 'Image_Overlay'
        image_opacity = 0.25
        image_url = 'data.png'
        min_lon, max_lon, min_lat, max_lat = -90.0, 90.0, -180.0, 180.0
        image_bounds = [[min_lon, min_lat], [max_lon, max_lat]]

        image_rendered = image_tpl.render({'image_name': image_name,
                                           'image_url': image_url,
                                           'image_bounds': image_bounds,
                                           'image_opacity': image_opacity})

        self.map.image_overlay(data, filename=image_url)
        assert image_rendered in self.map.template_vars['image_layers']

        image_rendered = image_tpl.render({'image_name': image_name,
                                           'image_url': inline_image_url,
                                           'image_bounds': image_bounds,
                                           'image_opacity': image_opacity})

        self.map.image_overlay(data)
        assert image_rendered in self.map.template_vars['image_layers']

    def test_scroll_zoom_toggler_plugin(self):
        """Test ScrollZoomToggler plugin."""
        a_map = folium.Map([45, 3], zoom_start=4)
        a_map.add_plugin(ScrollZoomToggler())
        a_map._build_map()

    def test_marker_cluster_plugin(self):
        """Test MarkerCluster plugin."""
        data = [(35, -12, "lower left"),
                (35, 30, "lower right"),
                (60, -12, "upper left"),
                (60, 30, "upper right"),
                ]
        a_map = folium.Map([0, 0], zoom_start=0)
        a_map.add_plugin(MarkerCluster(data))
        a_map._build_map()
