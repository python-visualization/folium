import random

import streamlit as st
from streamlit_folium import st_folium

import folium

st.set_page_config(layout="wide")


CENTER_START = [39.949610, -75.150282]
ZOOM_START = 8

if "center" not in st.session_state:
    st.session_state["center"] = [39.949610, -75.150282]
if "zoom" not in st.session_state:
    st.session_state["zoom"] = 8
if "markers" not in st.session_state:
    st.session_state["markers"] = []

col1, col2, col3 = st.columns(3)

if col1.button("Shift center"):
    random_shift_y = (random.random() - 0.5) * 0.3
    random_shift_x = (random.random() - 0.5) * 0.3
    st.session_state["center"] = [
        st.session_state["center"][0] + random_shift_y,
        st.session_state["center"][1] + random_shift_x,
    ]

if col2.button("Shift zoom"):
    st.session_state["zoom"] = st.session_state["zoom"] + 1
    if st.session_state["zoom"] >= 10:
        st.session_state["zoom"] = 5

if col3.button("Add random marker"):
    random_lat = random.random() * 0.5 + 39.8
    random_lon = random.random() * 0.5 - 75.2
    random_marker = folium.Marker(
        location=[random_lat, random_lon],
        popup=f"Random marker at {random_lat:.2f}, {random_lon:.2f}",
    )
    st.session_state["markers"].append(random_marker)

col1, col2 = st.columns(2)

with col1:
    "# New method"
    "### Pass `center`, `zoom`, and `feature_group_to_add` to `st_folium`"
    with st.echo(code_location="below"):
        m = folium.Map(location=CENTER_START, zoom_start=8)
        fg = folium.FeatureGroup(name="Markers")
        for marker in st.session_state["markers"]:
            fg.add_child(marker)

        st_folium(
            m,
            center=st.session_state["center"],
            zoom=st.session_state["zoom"],
            key="new",
            feature_group_to_add=fg,
            height=400,
            width=700,
        )

with col2:
    "# Old method"
    "### Update the map before passing it to `st_folium`"
    with st.echo(code_location="below"):
        m = folium.Map(
            location=st.session_state["center"], zoom_start=st.session_state["zoom"]
        )
        fg = folium.FeatureGroup(name="Markers")
        for marker in st.session_state["markers"]:
            fg.add_child(marker)
        m.add_child(fg)
        st_folium(
            m,
            key="old",
            height=400,
            width=700,
        )
