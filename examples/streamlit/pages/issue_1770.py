import json

import streamlit as st
from streamlit_folium import st_folium

import folium

st.set_page_config(layout="wide")

geojson = """
{"type": "FeatureCollection",
 "features": [
    {"id": "0", "type": "Feature", "properties": {"foo": 0},
     "geometry": {"type": "Point", "coordinates": [0.0, 0.0]}
    },
    {"id": "1", "type": "Feature", "properties": {"foo": 1},
     "geometry": {"type": "MultiPoint", "coordinates": [[1.0, 1.0]]}},
    {"id": "2", "type": "Feature",
 "properties": {"foo": 2}, "geometry": {"type": "MultiPoint", "coordinates":
 [[2.0, 2.0]]}}, {"id": "3", "type": "Feature", "properties": {"foo": 3},
 "geometry": {"type": "MultiPoint", "coordinates": [[3.0, 3.0]]}}, {"id": "4",
 "type": "Feature", "properties": {"foo": 4}, "geometry": {"type":
 "MultiPoint", "coordinates": [[4.0, 4.0]]}}]}"""

geojson = json.loads(geojson)

on_each_feature = folium.JsCode(
    """
    (feature, layer) => {
        layer.bindPopup("hello world");
    }
"""
)
m = folium.Map(
    zoom_start=5,
    location=(0, 0),
)
folium.GeoJson(
    geojson, on_each_feature=on_each_feature, marker=folium.CircleMarker(radius=20)
).add_to(m)

st_folium(m, width=700, height=500)
# st_folium(m, width=700, height=500, returned_objects=[])

html = m.get_root().render()
st.code(html)
