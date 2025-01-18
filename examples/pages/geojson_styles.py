import geopandas as gpd
import shapely
import streamlit as st
from streamlit_folium import st_folium

import folium

st.title("GeoJSON Styling")

START_LOCATION = [37.7934347109497, -122.399077892527]
START_ZOOM = 18

wkt = (
    "POLYGON ((-122.399077892527 37.7934347109497, -122.398922660838 "
    "37.7934544916178, -122.398980265018 37.7937266504805, -122.399133972495 "
    "37.7937070646238, -122.399077892527 37.7934347109497))"
)
polygon_ = shapely.wkt.loads(wkt)
gdf = gpd.GeoDataFrame(geometry=[polygon_]).set_crs(epsg=4326)

style_parcels = {"fillColor": "red", "fillOpacity": 0.2}

polygon_folium = folium.GeoJson(data=gdf, style_function=lambda x: style_parcels)

map = folium.Map(
    location=START_LOCATION, zoom_start=START_ZOOM, tiles="OpenStreetMap", max_zoom=21
)
fg = folium.FeatureGroup(name="Parcels")
fg = fg.add_child(polygon_folium)

st_folium(
    map,
    width=800,
    height=450,
    feature_group_to_add=fg,
    debug=True,
)
