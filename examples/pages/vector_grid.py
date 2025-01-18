import streamlit as st
from streamlit_folium import st_folium

import folium
from folium.plugins import VectorGridProtobuf

st.set_page_config(
    page_title="streamlit-folium documentation: Vector Grid",
)

with st.echo(code_location="below"):
    m = folium.Map(location=(30, 20), zoom_start=4)
    folium.Marker(location=(30, 20), popup="test").add_to(m)
    url = "https://area.uqcom.jp/api2/rakuten/{z}/{x}/{y}.mvt"
    vc = VectorGridProtobuf(url, "test").add_to(m)

    st_folium(m, returned_objects=[])
