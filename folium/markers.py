# -*- coding: utf-8 -*-
'''
Markers
-------

Folium module to create leaflet.js markers

'''

from __future__ import print_function
from __future__ import division
from jinja2 import Environment, PackageLoader, Template


def popup_render(popup_temp, mark_name, count, popup_txt, popup=True):
    '''Popup renderer'''
    if popup:
        popup = popup_temp.render({'pop_name': mark_name + str(count),
                                   'pop_txt': popup_txt})
    else:
        popup = 'var no_pop = null'
    return popup

def simple_marker(coords, popup_txt, popup, count):
    '''Define a simple Leaflet marker

    Parameters
    ----------
    coords: list or tuple
        Lat/Lon for marker position
    popup_txt: str
        Popup text
    popup: boolean
        True to include popup, False for no popup
    count: int
        Counter to generate a new marker on each iteration

    Returns
    -------
    Marker object HTML

    '''
    env = Environment(loader=PackageLoader('folium', 'templates'))
    mark_temp = env.get_template('simple_marker.txt')
    popup_temp = env.get_template('simple_popup.txt')

    #Get marker and popup
    marker = mark_temp.render({'marker': 'marker_' + str(count),
                               'lat': coords[0], 'lon': coords[1]})

    popup = popup_render(popup_temp, 'marker_', count, popup_txt, popup=popup)

    return (marker, popup)


def circle_marker(coords, radius, line_color, fill_color, fill_opacity,
                  popup_txt, popup, count):
    '''Define a Leaflet circle marker of given dimension and color

    Parameters
    ----------
    coords: list or tuple
        Lat/Lon for marker position
    radius: int
        Circle radius in pixels
    color: string
        Primary color (red, blue, etc) or hex code
    fill_color: string
        Primary color (red, blue, etc) or hex code
    fill_opacity: float
        Opacity value

    Returns
    -------
    Circle object HTML
    '''

    env = Environment(loader=PackageLoader('folium', 'templates'))
    circle_temp = env.get_template('circle_marker.txt')
    popup_temp = env.get_template('simple_popup.txt')

    circle = circle_temp.render({'circle': 'circle_' + str(count),
                                 'radius': radius,
                                 'lat': coords[0], 'lon': coords[1],
                                 'line_color': line_color,
                                 'fill_color': fill_color,
                                 'fill_opacity': fill_opacity})

    popup = popup_render(popup_temp, 'circle_', count, popup_txt, popup=popup)

    return (circle, popup)




