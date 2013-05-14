# -*- coding: utf-8 -*-
'''
Folium Tests
-------

'''
import nose.tools as nt
import folium
from jinja2 import Environment, PackageLoader


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




















