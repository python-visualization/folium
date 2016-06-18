# -*- coding: utf-8 -*-
import folium
from folium import plugins

m = folium.Map([30., 0.], zoom_start=3)
wind_locations = [[59.3556, -31.99219], [55.17887, -42.89062], [47.7541, -43.94531],
                  [38.27269, -37.96875], [27.05913, -41.13281], [16.29905, -36.5625],
                  [8.40717, -30.23437], [1.05463, -22.5], [-8.75479, -18.28125],
                  [-21.61658, -20.03906], [-31.35364, -24.25781], [-39.90974, -30.9375],
                  [-43.83453, -41.13281], [-47.7541, -49.92187], [-50.95843, -54.14062],
                  [-55.9738, -56.60156]]

wind_line = folium.PolyLine(wind_locations, weight=15, color='#8EE9FF').add_to(m)
attr = {'fill': '#007DEF', 'font-weight': 'bold', 'font-size': '24'}
plugins.PolyLineTextPath(wind_line, ") ", repeat=True, offset=7, attributes=attr).add_to(m)

danger_line = folium.PolyLine([[-40.311, -31.952], [-12.086, -18.727]], weight=10, color='orange',
                              opacity=0.8).add_to(m)
attr = {'fill': 'red'}
plugins.PolyLineTextPath(danger_line, "\u25BA", repeat=True, offset=6, attributes=attr).add_to(m)

plane_line = folium.PolyLine([[-49.38237, -37.26562], [-1.75754, -14.41406], [51.61802, -23.20312]],
                             weight=1, color='black').add_to(m)
attr = {'font-weight': 'bold', 'font-size': '24'}
plugins.PolyLineTextPath(plane_line, "\u2708     ", repeat=True, offset=8, attributes=attr).add_to(m)

line_to_new_delhi = folium.PolyLine([[46.67959447, 3.33984375],
                                     [46.5588603, 29.53125],
                                     [42.29356419, 51.328125],
                                     [35.74651226, 68.5546875],
                                     [28.65203063, 76.81640625]]).add_to(m)

line_to_hanoi = folium.PolyLine([[28.76765911, 77.60742188],
                                 [27.83907609, 88.72558594],
                                 [25.68113734, 97.3828125],
                                 [21.24842224, 105.77636719]]).add_to(m)

plugins.PolyLineTextPath(line_to_new_delhi, "To New Delhi", offset=-5).add_to(m)
plugins.PolyLineTextPath(line_to_hanoi, "To Hanoi", offset=-5).add_to(m)

m.save(outfile='polyline_text.html')
