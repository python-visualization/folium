import streamlit as st
from streamlit_folium import st_folium

import folium

st.set_page_config(
    layout="wide",
    page_title="streamlit-folium documentation: Misc Examples",
    page_icon="random",
)
"""
# streamlit-folium: Image Overlay

By default, st_folium renders images using browser image rendering mechanism.
Use st_folium(map, pixelated=True) in order to see image pixels without resample.
"""

url_image = "https://i.postimg.cc/kG2FSxSR/image.png"
image_bounds = [[-20.664910, -46.538223], [-20.660001, -46.532977]]

m = folium.Map()
m1 = folium.Map()

folium.raster_layers.ImageOverlay(
    image=url_image,
    name="image overlay",
    opacity=1,
    bounds=image_bounds,
).add_to(m)
folium.raster_layers.ImageOverlay(
    image=url_image,
    name="image overlay",
    opacity=1,
    bounds=image_bounds,
).add_to(m1)

m.fit_bounds(image_bounds, padding=(0, 0))
m1.fit_bounds(image_bounds, padding=(0, 0))

col1, col2 = st.columns(2)
with col1:
    st.markdown("## Pixelated off")
    st_folium(m, use_container_width=True, pixelated=False, key="pixelated_off")
with col2:
    st.markdown("## Pixelated on")
    st_folium(m1, use_container_width=True, pixelated=True, key="pixelated_on")
