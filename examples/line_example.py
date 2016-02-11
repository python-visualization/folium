# -*- coding: utf-8 -*-
'''Test of Folium polylines'''

import folium

# Coordinates are 15 points on the great circle from Boston to
# San Francisco.
# Reference: http://williams.best.vwh.net/avform.htm#Intermediate
coordinates = [
    [42.3581, -71.0636],
    [42.82995815, -74.78991444],
    [43.17929819, -78.56603306],
    [43.40320216, -82.37774519],
    [43.49975489, -86.20965845],
    [43.46811941, -90.04569087],
    [43.30857071, -93.86961818],
    [43.02248456, -97.66563267],
    [42.61228259, -101.41886832],
    [42.08133868, -105.11585198],
    [41.4338549, -108.74485069],
    [40.67471747, -112.29609954],
    [39.8093434, -115.76190821],
    [38.84352776, -119.13665678],
    [37.7833, -122.4167]]


# Create the map and add the line
m = folium.Map(location=[41.9, -97.3], zoom_start=4)
m.line(coordinates, line_color='#FF0000', line_weight=5)

m.create_map(path='line_example.html')
