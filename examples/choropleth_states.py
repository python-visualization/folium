'''
Choropleth maps of US states

'''

import folium
import json
import pandas as pd

state_geo = r'data/us-states.json'
state_unemployment = r'data/US_Unemployment_Oct2012.csv'

state_data = pd.read_csv(state_unemployment)

#Let Folium determine the scale
map = folium.Map(location=[48, -102], zoom_start=3)
map.geo_json(geo_path=state_geo, data=state_data,
             columns=['State', 'Unemployment'],
             key_on='feature.id',
             fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2)
map.create_map()

#Let's define our own scale
map.geo_json(geo_path=state_geo, data=state_data,
             columns=['State', 'Unemployment'],
             threshold_scale=[5, 6, 7, 8, 9, 10],
             key_on='feature.id',
             fill_color='YlGn', fill_opacity=0.7, line_opacity=0.5,
             legend_name='Unemployment Rate (%)',
             reset=True)
map.create_map()