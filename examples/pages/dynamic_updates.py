from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
import shapely
import streamlit as st
from streamlit_folium import st_folium

import folium
import folium.features

p = Path(__file__).parent / "states.csv"
STATE_DATA = pd.read_csv(p)


st.set_page_config(layout="wide")

"# Dynamic Updates -- Click on a marker"

st.subheader(
    "Use new arguments `center`, `zoom`, and `feature_group_to_add` to update the map "
    "without re-rendering it."
)


@st.cache_data
def _get_all_state_bounds() -> dict:
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    data = requests.get(url).json()
    return data


@st.cache_data
def get_state_bounds(state: str) -> dict:
    data = _get_all_state_bounds()
    state_entry = [f for f in data["features"] if f["properties"]["name"] == state][0]
    return {"type": "FeatureCollection", "features": [state_entry]}


def get_state_from_lat_lon(lat: float, lon: float) -> str:
    state_row = STATE_DATA[
        STATE_DATA.latitude.between(lat - 0.0001, lat + 0.0001)
        & STATE_DATA.longitude.between(lon - 0.0001, lon + 0.0001)
    ].iloc[0]
    return state_row["state"]


def get_population(state: str) -> int:
    return STATE_DATA.set_index("state").loc[state]["population"]


def main():
    if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None
    if "selected_state" not in st.session_state:
        st.session_state["selected_state"] = "Indiana"

    bounds = get_state_bounds(st.session_state["selected_state"])

    st.write(f"## {st.session_state['selected_state']}")
    population = get_population(st.session_state["selected_state"])
    st.write(f"### Population: {population:,}")

    center = None
    if st.session_state["last_object_clicked"]:
        center = st.session_state["last_object_clicked"]

    with st.echo(code_location="below"):
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

        # If you want to dynamically add or remove items from the map,
        # add them to a FeatureGroup and pass it to st_folium
        fg = folium.FeatureGroup(name="State bounds")
        fg.add_child(folium.features.GeoJson(bounds))

        capitals = STATE_DATA

        for capital in capitals.itertuples():
            fg.add_child(
                folium.Marker(
                    location=[capital.latitude, capital.longitude],
                    popup=f"{capital.capital}, {capital.state}",
                    tooltip=f"{capital.capital}, {capital.state}",
                    icon=(
                        folium.Icon(color="green")
                        if capital.state == st.session_state["selected_state"]
                        else None
                    ),
                )
            )

        out = st_folium(
            m,
            feature_group_to_add=fg,
            center=center,
            width=1200,
            height=500,
        )

    if (
        out["last_object_clicked"]
        and out["last_object_clicked"] != st.session_state["last_object_clicked"]
    ):
        st.session_state["last_object_clicked"] = out["last_object_clicked"]
        state = get_state_from_lat_lon(*out["last_object_clicked"].values())
        st.session_state["selected_state"] = state
        st.rerun()

    st.write("## Dynamic feature group updates")

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
    polygon_folium2 = folium.GeoJson(
        data=gdf2, style_function=lambda x: style_buildings
    )

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

    fg = st.radio("Feature Group", ["Parcels", "Buildings", "None", "Both"])

    st_folium(
        map,
        width=800,
        height=450,
        returned_objects=[],
        feature_group_to_add=fg_dict[fg],
        debug=True,
    )


if __name__ == "__main__":
    main()
