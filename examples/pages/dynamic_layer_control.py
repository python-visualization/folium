from __future__ import annotations

import geopandas as gpd
import shapely
import streamlit as st
from streamlit_folium import st_folium

import folium
import folium.features

st.set_page_config(layout="wide")

st.write("## Dynamic layer control updates")

START_LOCATION = [37.7944347109497, -122.398077892527]
START_ZOOM = 17

if "feature_group" not in st.session_state:
    st.session_state["feature_group"] = None

wkt1 = (
    "POLYGON ((-122.399077892527 37.7934347109497, -122.398922660838 "
    "37.7934544916178, -122.398980265018 37.7937266504805, -122.399133972495 "
    "37.7937070646238, -122.399077892527 37.7934347109497))"
)
wkt2 = (
    "POLYGON ((-122.397416 37.795017, -122.397137 37.794712, -122.396332 37.794983,"
    " -122.396171 37.795483, -122.396858 37.795695, -122.397652 37.795466, "
    "-122.397759 37.79511, -122.397416 37.795017))"
)

polygon_1 = shapely.wkt.loads(wkt1)
polygon_2 = shapely.wkt.loads(wkt2)

gdf1 = gpd.GeoDataFrame(geometry=[polygon_1]).set_crs(epsg=4326)
gdf2 = gpd.GeoDataFrame(geometry=[polygon_2]).set_crs(epsg=4326)

style_parcels = {
    "fillColor": "#1100f8",
    "color": "#1100f8",
    "fillOpacity": 0.13,
    "weight": 2,
}
style_buildings = {
    "color": "#ff3939",
    "fillOpacity": 0,
    "weight": 3,
    "opacity": 1,
    "dashArray": "5, 5",
}

polygon_folium1 = folium.GeoJson(data=gdf1, style_function=lambda x: style_parcels)
polygon_folium2 = folium.GeoJson(data=gdf2, style_function=lambda x: style_buildings)

map = folium.Map(
    location=START_LOCATION,
    zoom_start=START_ZOOM,
    tiles="OpenStreetMap",
    max_zoom=21,
)

fg1 = folium.FeatureGroup(name="Parcels")
fg1.add_child(polygon_folium1)

fg2 = folium.FeatureGroup(name="Buildings")
fg2.add_child(polygon_folium2)

fg_dict = {"Parcels": fg1, "Buildings": fg2, "None": None, "Both": [fg1, fg2]}

control = folium.LayerControl(collapsed=False)

fg = st.radio("Feature Group", ["Parcels", "Buildings", "None", "Both"])

layer = st.radio("Layer Control", ["yes", "no"])

layer_dict = {"yes": control, "no": None}

st_folium(
    map,
    width=800,
    height=450,
    returned_objects=[],
    feature_group_to_add=fg_dict[fg],
    debug=True,
    layer_control=layer_dict[layer],
)
