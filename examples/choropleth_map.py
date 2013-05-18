import folium
import json
import pandas as pd
import vincent

county_data = r'data/us_county_data.csv'
county_geo = r'data/us-counties.json'
state_geo = r'data/us-states.json'
state_unemployment = r'data/US_Unemployment_Oct2012.csv'

#We want to map the county codes we have in our geometry to those in the
#county_data file, which contains additional rows we don't need
with open(county_geo, 'r') as f:
    get_id = json.load(f)

county_codes = [x['id'] for x in get_id['features']]
county_df = pd.DataFrame({'FIPS_Code': county_codes}, dtype=str)

#Read into Dataframe, cast to string for consistency
df = pd.read_csv(county_data, na_values=[' '])
df['FIPS_Code'] = df['FIPS_Code'].astype(str)

#Perform an inner join, pad NA's with data from nearest county
merged = pd.merge(df, county_df, on='FIPS_Code', how='inner')
merged = merged.fillna(method='pad')

#Number of employed with auto scale
map = folium.Map(location=[48, -102], zoom_start=3)
map.geo_json(geo_path=county_geo, data=merged,
             columns=['FIPS_Code', 'Employed_2011'], key_on='feature.id',
             fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2)
map.create_map()

#Unemployment with custom defined scale
map = folium.Map(location=[40, -99], zoom_start=4)
map.geo_json(geo_path=county_geo, data=merged,
             columns=['FIPS_Code', 'Unemployment_rate_2011'],
             key_on='feature.id',
             threshold_scale=[0, 5, 7, 9, 11, 13],
             fill_color='YlGnBu', line_opacity=0.3,
             legend_name='Unemployment Rate 2011 (%)')
map.create_map()
