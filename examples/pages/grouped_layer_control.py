import streamlit as st
from streamlit_folium import st_folium

import folium
from folium.plugins import GroupedLayerControl

st.set_page_config(
    page_title="streamlit-folium documentation: Grouped Layer Control",
    page_icon=":pencil:",
    layout="wide",
)

st.title("streamlit-folium: Grouped Layer Control")

m = folium.Map([40.0, 70.0], zoom_start=6)

fg1 = folium.FeatureGroup(name="g1")
fg2 = folium.FeatureGroup(name="g2")
fg3 = folium.FeatureGroup(name="g3")
folium.Marker([40, 74]).add_to(fg1)
folium.Marker([38, 72]).add_to(fg2)
folium.Marker([40, 72]).add_to(fg3)
m.add_child(fg1)
m.add_child(fg2)
m.add_child(fg3)

folium.LayerControl(collapsed=False).add_to(m)

GroupedLayerControl(
    groups={"groups1": [fg1, fg2]},
    collapsed=False,
).add_to(m)

st_folium(m)
