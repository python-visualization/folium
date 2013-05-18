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

map = folium.Map(location=[39.8282, -98.5795], zoom_start=4)
map.geo_json(county_geo, data=merged,
             columns=['FIPS_Code', 'Unemployed_2011'], key_on='feature.id',
             fill_color='YlGnBu', line_opacity=0.4,
             quantize_range=[0, 5000])
map.create_map()
