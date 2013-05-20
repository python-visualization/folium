# -*- coding: utf-8 -*-
'''Folium Vincent plotting'''

import pandas as pd
import vincent
import folium

NOAA_46041 = pd.read_csv(r'data/NOAA_46041.csv', index_col=3,
                         parse_dates=True)
NOAA_46050 = pd.read_csv(r'data/NOAA_46050_WS.csv', index_col=3,
                         parse_dates=True)
NOAA_46243 = pd.read_csv(r'data/NOAA_46243.csv', index_col=3,
                         parse_dates=True)

#Binned wind speeds for NOAA 46050
bins = range(0, 13, 1)
cuts = pd.cut(NOAA_46050['wind_speed_cwind (m/s)'], bins)
ws_binned = pd.value_counts(cuts).reindex(cuts.levels)

#NOAA 46401 Wave Period
vis1 = vincent.Line(width=600)
vis1.tabular_data(NOAA_46041, columns=['dominant_wave_period (s)'],
                  axis_time='day')
vis1.axis_label(x_label='Time', y_label='Dominant Wave Period (s)')
vis1.to_json('vis1.json')

#NOAA 46050 Binned Wind Speed
vis2 = vincent.Bar(width=600)
vis2.tabular_data(ws_binned)
vis2.axis_label(x_label='Wind Speed (m/s)', y_label='# of Obs')
vis2 -= ('hover', 'marks', 0, 'properties')
vis2.to_json('vis2.json')

#NOAA 46243 Wave Height
vis3 = vincent.Area(width=600)
vis3.tabular_data(NOAA_46243, columns=['significant_wave_height (m)'],
                  axis_time='day')
vis3 -= ('hover', 'marks', 0, 'properties')
vis3.axis_label(x_label='Time', y_label='Significant Wave Height (m)')
vis3.to_json('vis3.json')

#Map all buoys
buoy_map = folium.Map(location=[46.3014, -123.7390], zoom_start=7,
                      tiles='Stamen Terrain')
buoy_map.polygon_marker(location=[47.3489, -124.708], fill_color='#43d9de',
                        radius=12, popup=(vis1, 'vis1.json'))
buoy_map.polygon_marker(location=[44.639, -124.5339], fill_color='#43d9de',
                        radius=12, popup=(vis2, 'vis2.json'))
buoy_map.polygon_marker(location=[46.216, -124.1280], fill_color='#43d9de',
                        radius=12, popup=(vis3, 'vis3.json'))
buoy_map.create_map(path='NOAA_buoys.html')
