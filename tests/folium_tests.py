# -*- coding: utf-8 -*-
'''
Folium Tests
-------

'''
import json
import pandas as pd
import nose.tools as nt
import folium
from jinja2 import Environment, PackageLoader

def setup_data():
    '''Import economic data for testing'''
    with open('us-counties.json', 'r') as f:
       get_id = json.load(f)

    county_codes = [x['id'] for x in get_id['features']]
    county_df = pd.DataFrame({'FIPS_Code': county_codes}, dtype=str)

    #Read into Dataframe, cast to string for consistency
    df = pd.read_csv('us_county_data.csv', na_values=[' '])
    df['FIPS_Code'] = df['FIPS_Code'].astype(str)

    #Perform an inner join, pad NA's with data from nearest county
    merged = pd.merge(df, county_df, on='FIPS_Code', how='inner')
    return merged.fillna(method='pad')


class testFolium(object):
    '''Test class for the Folium library'''

    def setup(self):
        '''Setup Folium Map'''

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

        tmpl = {'Tiles': u'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attr': (u'Map data \xa9 <a href="http://openstreetmap.org">'
                         'OpenStreetMap</a> contributors'),
                'lat': 45.5236, 'lon': -122.675, 'max_zoom': 20,
                'size': 'style="width: 900px; height: 400px"',
                'zoom_level': 4}

        assert self.map.template_vars == tmpl

    def test_cloudmade(self):
        '''Test cloudmade tiles and the API key'''

        nt.assert_raises(ValueError, callableObj=folium.Map,
                         location=[45.5236, -122.6750], tiles='cloudmade')

        map = folium.Map(location=[45.5236, -122.6750], tiles='cloudmade',
                         API_key='###')
        assert map.template_vars['Tiles'] == (u'http://{s}.tile.cloudmade.com'
                                              '/###/997/256/{z}/{x}/{y}.png')

    def test_builtin_tile(self):
        '''Test custom maptiles'''

        default_tiles = ['OpenStreetMap', 'Mapbox', 'Mapbox Dark']
        for tiles in default_tiles:
            map = folium.Map(location=[45.5236, -122.6750], tiles=tiles)
            tiles = ''.join(tiles.lower().strip().split())
            url = map.tile_types[tiles]['templ'].render()
            attr = map.tile_types[tiles]['attr'].render()

            assert map.template_vars['Tiles'] == url
            assert map.template_vars['attr'] == attr

    def test_custom_tile(self):
        '''Test custom tile URLs'''

        url = u'http://{s}.custom_tiles.org/{z}/{x}/{y}.png'
        attr = 'Attribution for custom tiles'

        nt.assert_raises(ValueError, callableObj=folium.Map,
                         location=[45.5236, -122.6750], tiles=url)

        map = folium.Map(location=[45.52, -122.67], tiles=url, attr=attr)
        assert map.template_vars['Tiles'] == url
        assert map.template_vars['attr'] == attr

    def test_simple_marker(self):
        '''Test simple marker addition'''

        mark_templ = self.env.get_template('simple_marker.txt')
        popup_templ = self.env.get_template('simple_popup.txt')

        #Single Simple marker
        self.map.simple_marker(location=[45.50, -122.7])
        mark_1 = mark_templ.render({'marker': 'marker_1', 'lat': 45.50,
                                    'lon': -122.7})
        popup_1 = popup_templ.render({'pop_name': 'marker_1',
                                      'pop_txt': 'Pop Text'})
        assert self.map.template_vars['markers'][0][0] == mark_1
        assert self.map.template_vars['markers'][0][1] == popup_1

        #Test Simple marker addition
        self.map.simple_marker(location=[45.60, -122.8], popup_txt='Hi')
        mark_2 = mark_templ.render({'marker': 'marker_2', 'lat': 45.60,
                                    'lon': -122.8})
        popup_2 = popup_templ.render({'pop_name': 'marker_2',
                                      'pop_txt': 'Hi'})
        assert self.map.mark_cnt['simple'] == 2
        assert self.map.template_vars['markers'][1][0] == mark_2
        assert self.map.template_vars['markers'][1][1] == popup_2

        #Test no popup
        self.map.simple_marker(location=[45.60, -122.8], popup=False)
        assert self.map.template_vars['markers'][2][1] == 'var no_pop = null'

    def test_circle_marker(self):
        '''Test circle marker additions'''

        circ_templ = self.env.get_template('circle_marker.txt')

        #Single Circle marker
        self.map.circle_marker(location=[45.60, -122.8], popup_txt='Hi')
        circle_1 = circ_templ.render({'circle': 'circle_1', 'lat': 45.60,
                                      'lon': -122.8, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert self.map.template_vars['markers'][0][0] == circle_1

        #Second circle marker
        self.map.circle_marker(location=[45.70, -122.9], popup_txt='Hi')
        circle_2 = circ_templ.render({'circle': 'circle_2', 'lat': 45.70,
                                      'lon': -122.9, 'radius': 500,
                                      'line_color': 'black',
                                      'fill_color': 'black',
                                      'fill_opacity': 0.6})
        assert self.map.template_vars['markers'][1][0] == circle_2

    def test_latlng_pop(self):
        '''Test lat/lon popovers'''

        self.map.lat_lng_popover()
        pop_templ = self.env.get_template('lat_lng_popover.txt').render()
        assert self.map.template_vars['lat_lng_pop'] == pop_templ

    def test_click_for_marker(self):
        '''Test click for marker functionality'''

        #lat/lng popover
        self.map.click_for_marker()
        click_templ = self.env.get_template('click_for_marker.txt')
        click = click_templ.render({'popup': ('"Latitude: " + lat + "<br>'
                                              'Longitude: " + lng ')})
        assert self.map.template_vars['click_pop'] == click

        #Custom popover
        self.map.click_for_marker(popup_txt='Test')
        click_templ = self.env.get_template('click_for_marker.txt')
        click = click_templ.render({'popup': '"Test"'})
        assert self.map.template_vars['click_pop'] == click

    def test_geo_json(self):
        '''Test geojson  method'''

        path = 'us-counties.json'
        geo_path = ".defer(d3.json, '{0}')".format(path)

        #No data binding
        self.map.geo_json(path)
        geo_path = ".defer(d3.json, '{0}')".format(path)
        map_var = 'gjson_1'
        style_temp = self.env.get_template('geojson_style.txt')
        style = style_temp.render({'style': 'style_1',
                                   'line_color': 'black',
                                   'line_weight': 1,
                                   'line_opacity': 1,
                                   'fill_color': 'blue',
                                   'fill_opacity': 0.6})
        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2}}}).addTo(map)'
                 .format(1, map_var, 'style_1'))

        templ = self.map.template_vars
        assert self.map.map_type == 'geojson'
        assert templ['func_vars'][0] == map_var
        assert templ['geo_styles'][0] == style
        assert templ['gjson_layers'][0] == layer
        assert templ['json_paths'][0] == geo_path

        #With DataFrame data binding, default quantize scale
        data = setup_data()
        self.map.geo_json(path, data=data,
                          columns=['FIPS_Code', 'Unemployed_2011'],
                          key_on='feature.id', fill_color='YlGnBu',
                          reset=True)
        geo_path = ".defer(d3.json, '{0}')".format(path)
        data_path = ".defer(d3.json, '{0}')".format('data.json')
        map_var = 'gjson_1'
        data_var = 'data_1'
        style_temp = self.env.get_template('geojson_style.txt')
        color = 'color(matchKey(feature.id, data_1))'
        style = style_temp.render({'style': 'style_1',
                                   'line_color': 'black',
                                   'line_weight': 1,
                                   'line_opacity': 1,
                                   'fill_color': color,
                                   'fill_opacity': 0.6})
        layer = ('gJson_layer_{0} = L.geoJson({1}, {{style: {2}}}).addTo(map)'
                 .format(1, map_var, 'style_1'))

        templ = self.map.template_vars
        assert templ['func_vars'] == [data_var, map_var]
        assert templ['geo_styles'] == style
        assert templ['gjson_layers'] == layer
        assert templ['json_paths'] == [data_path, geo_path]
        assert templ['']























