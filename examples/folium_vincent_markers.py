# -*- coding: utf-8 -*-
'''Folium Vincent plotting'''

import pandas as pd
import vincent
import folium

NOAA_46041 = pd.read_csv(r'NOAA_46041.csv', index_col=3,
                         parse_dates=True)
NOAA_46050 = pd.read_csv(r'NOAA_46050_WS.csv', index_col=3,
                         parse_dates=True)
NOAA_46243 = pd.read_csv(r'NOAA_46243.csv', index_col=3,
                         parse_dates=True)

NOAA_46041 = NOAA_46041.dropna()

# Binned wind speeds for NOAA 46050.
bins = range(0, 13, 1)
cuts = pd.cut(NOAA_46050['wind_speed_cwind (m/s)'], bins)
ws_binned = pd.value_counts(cuts).reindex(cuts.values.categories)

# NOAA 46401 Wave Period.
vis1 = vincent.Line(NOAA_46041['dominant_wave_period (s)'],
                    width=400, height=200)
vis1.axis_titles(x='Time', y='Dominant Wave Period (s)')
vis1.to_json('vis1.json')

# NOAA 46050 Binned Wind Speed.
vis2 = vincent.Bar(ws_binned, width=400, height=200)
vis2.axis_titles(x='Wind Speed (m/s)', y='# of Obs')
vis2.to_json('vis2.json')

# NOAA 46243 Wave Height.
vis3 = vincent.Area(NOAA_46243['significant_wave_height (m)'],
                    width=400, height=200)
vis3.axis_titles(x='Time', y='Significant Wave Height (m)')
vis3.to_json('vis3.json')

# Map all buoys similar to https://github.com/python-visualization/folium#vincentvega-markers
kw = dict(fill_color='#43d9de', radius=12)
buoy_map = folium.Map(location=[46.3014, -123.7390],
                      zoom_start=7, tiles='Stamen Terrain')

popup1 = folium.Popup(max_width=800).add_child(folium.Vega(vis1, width=500, height=250))
folium.RegularPolygonMarker([47.3489, -124.708], popup=popup1, **kw).add_to(buoy_map)

popup2 = folium.Popup(max_width=800).add_child(folium.Vega(vis2, width=500, height=250))
folium.RegularPolygonMarker([44.639, -124.5339], popup=popup2, **kw).add_to(buoy_map)

popup3 = folium.Popup(max_width=800).add_child(folium.Vega(vis3, width=500, height=250))
folium.RegularPolygonMarker([46.216, -124.1280], popup=popup3, **kw).add_to(buoy_map)

buoy_map.save(outfile='NOAA_buoys.html')
