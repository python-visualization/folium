# -*- coding: utf-8 -*-
'''
Folium Tests
-------

'''
import json
import mock
import pandas as pd
import nose.tools as nt
import jinja2
from jinja2 import Environment, PackageLoader
import vincent
import folium
from folium.six import PY3


def setup_data():
    '''Import economic data for testing'''
    with open('us-counties.json', 'r') as f:
        get_id = json.load(f)

    county_codes = [x['id'] for x in get_id['features']]
    county_df = pd.DataFrame({'FIPS_Code': county_codes}, dtype=str)

    # Read into Dataframe, cast to string for consistency.
    df = pd.read_csv('us_county_data.csv', na_values=[' '])
    df['FIPS_Code'] = df['FIPS_Code'].astype(str)

    # Perform an inner join, pad NA's with data from nearest county.
    merged = pd.merge(df, county_df, on='FIPS_Code', how='inner')
    return merged.fillna(method='pad')


def test_get_templates():
    '''Test template getting'''

    env = folium.utilities.get_templates()
    nt.assert_is_instance(env, jinja2.environment.Environment)


class testFolium(object):
    '''Test class for the Folium library'''

    def setup(self):
        '''Setup Folium Map'''
        with mock.patch('folium.folium.uuid4') as uuid4:
            uuid4().hex = '0' * 32
            self.map = folium.Map(location=[45.5236, -122.6750], width=900,
                                  height=400, max_zoom=20, zoom_start=4)
        self.env = Environment(loader=PackageLoader('folium', 'templates'))

    def test_init(self):
        '''Test map initialization'''

        assert self.map.map_type == 'base'
        assert self.map.mark_cnt == {}
        assert self.map.location == [45.5236, -122.6750]
        assert self.map.map_size == {'width': 900, 'height': 400}

        nt.assert_raises(ValueError, callableObj=folium.Map)

        tmpl = {'Tiles': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attr': ('Map data (c) <a href="http://openstreetmap.org">'
                         'OpenStreetMap</a> contributors'),
                'map_id': 'folium_' + '0' * 32,
                'lat': 45.5236,
                'lon': -122.675,
                'max_zoom': 20,
                'size': 'style="width: 900px; height: 400px"',
                'zoom_level': 4,
                'tile_layers': [],
                'wms_layers': [],
                'min_zoom': 1,
                'min_lat': -90,
                'max_lat': 90,
                'min_lon': -180,
                'max_lon': 180}

        assert self.map.template_vars == tmpl

    def test_cloudmade(self):
        '''Test cloudmade tiles and the API key'''

        nt.assert_raises(ValueError, callableObj=folium.Map,
                         location=[45.5236, -122.6750], tiles='cloudmade')

        map = folium.Map(location=[45.5236, -122.6750], tiles='cloudmade',
                         API_key='###')
        assert map.template_vars['Tiles'] == ('http://{s}.tile.cloudmade.com'
                                              '/###/997/256/{z}/{x}/{y}.png')

    def test_builtin_tile(self):
        '''Test custom maptiles'''

        default_tiles = ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner']
        for tiles in default_tiles:
            map = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = ''.join(tiles.lower().strip().split())
            url = map.tile_types[tiles]['templ'].render()
            attr = map.tile_types[tiles]['attr'].render()

            assert map.template_vars['Tiles'] == url
            assert map.template_vars['attr'] == attr

    def test_custom_tile(self):
        '''Test custom tile URLs'''

        url = 'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
        attr = 'Attribution for custom tiles'

        nt.assert_raises(ValueError, callableObj=folium.Map,
                         location=[45.5236, -122.6750], tiles=url)

        map = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert map.template_vars['Tiles'] == url
        assert map.template_vars['attr'] == attr

    def test_wms_layer(self):
        '''Test wms layer URLs'''

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
        wms = wms_temp.render({'wms_name': wms_name,
                               'wms_url': wms_url,
                               'wms_format': wms_format,
                               'wms_layer_names': wms_layers,
                               'wms_transparent': 'true'})
        assert map.template_vars['wms_layers'][0] == wms

    def test_simple_marker(self):
        '''Test simple marker addition'''

        mark_templ = self.env.get_template('simple_marker.js')
        popup_templ = self.env.get_template('simple_popup.js')

        # Single Simple marker.
        self.map.simple_marker(location=[45.50, -122.7])
        mark_1 = mark_templ.render({'marker': 'marker_1', 'lat': 45.50,
                                    'lon': -122.7,
                                    'icon': "{'icon':marker_1_icon}"})
        popup_1 = popup_templ.render({'pop_name': 'marker_1',
                                      'pop_txt': json.dumps('Pop Text'),
                                      'width': 300})
        assert self.map.template_vars['custom_markers'][0][1] == mark_1
        assert self.map.template_vars['custom_markers'][0][2] == popup_1

        # Test Simple marker addition.
        self.map.simple_marker(location=[45.60, -122.8], popup='Hi')
        mark_2 = mark_templ.render({'marker': 'marker_2', 'lat': 45.60,
                                    'lon': -122.8,
                                    'icon': "{'icon':marker_2_icon}"})
        popup_2 = popup_templ.render({'pop_name': 'marker_2',
                                      'pop_txt': json.dumps('Hi'),
                                      'width': 300})
        assert self.map.mark_cnt['simple'] == 2
        assert self.map.template_vars['custom_markers'][1][1] == mark_2
        assert self.map.template_vars['custom_markers'][1][2] == popup_2

        # Test no popup.
        self.map.simple_marker(location=[45.60, -122.8], popup_on=False)
        nopopup = 'var no_pop = null;'
        assert self.map.template_vars['custom_markers'][2][2] == nopopup

    def test_circle_marker(self):
        '''Test circle marker additions'''

        circ_templ = self.env.get_template('circle_marker.js')

        # Single Circle marker.
        self.map.circle_marker(location=[45.60, -122.8], popup='Hi')
        circle_1 = circ_templ.render({'circle': 'circle_1', 'lat': 45.60,
                                      'lon': -122.8, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert self.map.template_vars['markers'][0][0] == circle_1

        # Second circle marker.
        self.map.circle_marker(location=[45.70, -122.9], popup='Hi')
        circle_2 = circ_templ.render({'circle': 'circle_2', 'lat': 45.70,
                                      'lon': -122.9, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert self.map.template_vars['markers'][1][0] == circle_2

    def test_poly_marker(self):
        '''Test polygon marker'''

        poly_temp = self.env.get_template('poly_marker.js')

        polygon = poly_temp.render({'marker': 'polygon_1',
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

        self.map.polygon_marker(location=[45.5, -122.5])
        assert self.map.template_vars['markers'][0][0] == polygon

    def test_latlng_pop(self):
        '''Test lat/lon popovers'''

        self.map.lat_lng_popover()
        pop_templ = self.env.get_template('lat_lng_popover.js').render()
        assert self.map.template_vars['lat_lng_pop'] == pop_templ

    def test_click_for_marker(self):
        '''Test click for marker functionality'''

        # Lat/lon popover.
        self.map.click_for_marker()
        click_templ = self.env.get_template('click_for_marker.js')
        click = click_templ.render({'popup': ('"Latitude: " + lat + "<br>'
                                              'Longitude: " + lng ')})
        assert self.map.template_vars['click_pop'] == click

        # Custom popover.
        self.map.click_for_marker(popup='Test')
        click_templ = self.env.get_template('click_for_marker.js')
        click = click_templ.render({'popup': '"Test"'})
        assert self.map.template_vars['click_pop'] == click

    def test_vega_popup(self):
        '''Test vega popups'''

        vis = vincent.Bar(width=675 - 75, height=350 - 50, no_data=True)

        self.map.simple_marker(location=[45.60, -122.8],
                               popup=(vis, 'vis.json'))
        popup_temp = self.env.get_template('vega_marker.js')
        vega = popup_temp.render({'mark': 'marker_1', 'div_id': 'vis',
                                  'width': 675, 'height': 350,
                                  'max_width': 900,
                                  'json_out': 'vis.json',
                                  'vega_id': '#vis'})
        assert self.map.template_vars['custom_markers'][0][2] == vega

    def test_geo_json(self):
        '''Test geojson method'''

        path = 'us-counties.json'
        geo_path = ".defer(d3.json, '{0}')".format(path)

        # No data binding.
        self.map.geo_json(geo_path=path)
        geo_path = ".defer(d3.json, '{0}')".format(path)
        map_var = 'gjson_1'
        layer_var = 'gjson_1'
        style_temp = self.env.get_template('geojson_style.js')
        style = style_temp.render({'style': 'style_1',
                                   'line_color': 'black',
                                   'line_weight': 1,
                                   'line_opacity': 1,
                                   'fill_color': 'blue',
                                   'fill_opacity': 0.6})
        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2},'
                 'onEachFeature: onEachFeature}}).addTo(map)'
                 .format(1, layer_var, 'style_1'))

        templ = self.map.template_vars
        assert self.map.map_type == 'geojson'
        assert templ['func_vars'][0] == map_var
        assert templ['geo_styles'][0] == style
        assert templ['gjson_layers'][0] == layer
        assert templ['json_paths'][0] == geo_path

        # Data binding incorrect color value error.
        data = setup_data()
        nt.assert_raises(ValueError, self.map.geo_json,
                         path, data=data,
                         columns=['FIPS_Code', 'Unemployed_2011'],
                         key_on='feature.id', fill_color='blue')

        # Data binding threshold_scale too long.
        data = setup_data()
        nt.assert_raises(ValueError, self.map.geo_json,
                         path, data=data,
                         columns=['FIPS_Code', 'Unemployed_2011'],
                         key_on='feature.id',
                         threshold_scale=[1, 2, 3, 4, 5, 6, 7],
                         fill_color='YlGnBu')

        # With DataFrame data binding, default threshold scale.
        self.map.geo_json(geo_path=path, data=data,
                          columns=['FIPS_Code', 'Unemployed_2011'],
                          key_on='feature.id', fill_color='YlGnBu',
                          reset=True)
        geo_path = ".defer(d3.json, '{0}')".format(path)
        data_path = ".defer(d3.json, '{0}')".format('data.json')
        map_var = 'gjson_1'
        layer_var = 'gjson_1'
        data_var = 'data_1'

        domain = [4.0, 1000.0, 3000.0, 5000.0, 9000.0]
        palette = folium.utilities.color_brewer('YlGnBu')
        d3range = palette[0: len(domain) + 1]
        color_temp = self.env.get_template('d3_threshold.js')
        scale = color_temp.render({'domain': domain,
                                   'range': d3range})

        style_temp = self.env.get_template('geojson_style.js')
        color = 'color(matchKey(feature.id, data_1))'
        style = style_temp.render({'style': 'style_1',
                                   'line_color': 'black',
                                   'line_weight': 1,
                                   'line_opacity': 1,
                                   'quantize_fill': color,
                                   'fill_opacity': 0.6})

        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2},'
                 'onEachFeature: onEachFeature}}).addTo(map)'
                 .format(1, layer_var, 'style_1'))

        templ = self.map.template_vars
        assert templ['func_vars'] == [data_var, map_var]
        assert templ['geo_styles'][0] == style
        assert templ['gjson_layers'][0] == layer
        assert templ['json_paths'] == [data_path, geo_path]
        assert templ['color_scales'][0] == scale

        # Adding TopoJSON as additional layer.
        path_2 = 'or_counties_topo.json'
        self.map.geo_json(geo_path=path_2, topojson='objects.or_counties_geo')
        geo_path_2 = ".defer(d3.json, '{0}')".format(path_2)
        map_var_2 = 'tjson_2'
        layer_var_2 = 'topo_2'
        topo_func = ('topo_2 = topojson.feature(tjson_2,'
                     ' tjson_2.objects.or_counties_geo);')
        fmt = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2},'
               'onEachFeature: onEachFeature}}).addTo(map)')
        layer_2 = fmt.format(2, layer_var_2, 'style_2')

        templ = self.map.template_vars
        assert templ['func_vars'] == [data_var, map_var, map_var_2]
        assert templ['gjson_layers'][1] == layer_2
        assert templ['json_paths'] == [data_path, geo_path, geo_path_2]
        assert templ['topo_convert'][0] == topo_func

    def test_map_build(self):
        '''Test map build'''

        # Standard map.
        self.map._build_map()
        html_templ = self.env.get_template('fol_template.html')

        tmpl = {'Tiles': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attr': ('Map data (c) <a href="http://openstreetmap.org">'
                         'OpenStreetMap</a> contributors'),
                'map_id': 'folium_' + '0' * 32,
                'lat': 45.5236, 'lon': -122.675, 'max_zoom': 20,
                'size': 'style="width: 900px; height: 400px"',
                'zoom_level': 4,
                'min_zoom': 1,
                'min_lat': -90,
                'max_lat': 90,
                'min_lon': -180,
                'max_lon': 180}
        HTML = html_templ.render(tmpl)

        assert self.map.HTML == HTML

    def test_tile_attr_unicode(self):
        '''Test tile attribution unicode

        Test not cover b'юникод'
        because for python 3 bytes can only contain ASCII literal characters.
        '''

        if not PY3:
            map = folium.Map(location=[45.5236, -122.6750],
                             tiles='test', attr=b'unicode')
            map._build_map()
        else:
            map = folium.Map(location=[45.5236, -122.6750],
                             tiles='test', attr=u'юникод')
            map._build_map()
        map = folium.Map(location=[45.5236, -122.6750],
                         tiles='test', attr='юникод')
        map._build_map()

    def test_create_map(self):
        '''Test create map'''

        map = folium.Map(location=[45.5236, -122.6750],
                         tiles='test', attr='юникод')

        # Add json data
        path = 'us-counties.json'
        data = setup_data()
        map.geo_json(geo_path=path, data=data,
                     columns=['FIPS_Code', 'Unemployed_2011'],
                     key_on='feature.id', fill_color='YlGnBu',
                     reset=True)

        # Add plugins
        map.polygon_marker(location=[45.5, -122.5])

        # Test write
        map.create_map()

    def test_line(self):
        '''Test multi_polyline'''

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
            'locations': locations, 'options': line_opts})

        self.map.line(locations=locations,
           line_color=line_opts['color'],
           line_weight=line_opts['weight'],
           line_opacity=line_opts['opacity'])
        assert self.map.template_vars['lines'][0][0] == line_rendered

    def test_multi_polyline(self):
        '''Test multi_polyline'''

        multiline_temp = self.env.get_template('multi_polyline.js')

        multiline_opts = {'color': 'blue',
                'weight': 2,
                'opacity': 1}
        locations = [
                        [[45.5236, -122.6750], [45.5236, -122.6751]],
                        [[45.5237, -122.6750], [45.5237, -122.6751]],
                        [[45.5238, -122.6750], [45.5238, -122.6751]]
                    ]
        multiline_rendered = multiline_temp.render({'multiline': 'multiline_1',
                                                    'locations': locations,
                                                    'options': multiline_opts})

        self.map.multiline(locations=locations,
                           line_color=multiline_opts['color'],
                           line_weight=multiline_opts['weight'],
                           line_opacity=multiline_opts['opacity'])
        assert self.map.template_vars['multilines'][0][0] == multiline_rendered

    def test_fit_bounds(self):
        """Test fit_bounds"""
        bounds = ((52.193636, -2.221575), (52.636878, -1.139759))
        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
           'bounds': json.dumps(bounds),
           'fit_bounds_options': {},
        })

        self.map.fit_bounds(bounds)
        assert self.map.template_vars['fit_bounds'] == fit_bounds_rendered

        fit_bounds_tpl = self.env.get_template('fit_bounds.js')
        fit_bounds_rendered = fit_bounds_tpl.render({
           'bounds': json.dumps(bounds),
           'fit_bounds_options': json.dumps({'padding': (3,3), 'maxZoom': 15}),
        })

        self.map.fit_bounds(bounds, max_zoom=15, padding=(3, 3))
        assert self.map.template_vars['fit_bounds'] == fit_bounds_rendered

