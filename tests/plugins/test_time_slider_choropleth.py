"""
tests TimeSliderChoropleth
--------------------------

"""

import json

import numpy as np
import pandas as pd
from branca.colormap import linear

import folium
from folium.plugins import TimeSliderChoropleth
from folium.utilities import normalize


def test_timedynamic_geo_json():
    """
    tests folium.plugins.TimeSliderChoropleth
    """
    import geopandas as gpd

    assert "naturalearth_lowres" in gpd.datasets.available
    datapath = gpd.datasets.get_path("naturalearth_lowres")
    gdf = gpd.read_file(datapath)

    """
    Timestamps, start date is carefully chosen to be earlier than 2001-09-09
    (9 digit timestamp), end date is later (10 digits). This is to ensure an
    integer sort is used (and not a string sort were '2' > '10').
    datetime.strftime('%s') on Windows just generates date and not timestamp so avoid.
    """
    n_periods = 3
    dt_range = pd.Series(pd.date_range("2001-08-1", periods=n_periods, freq="M"))
    dt_index = [f"{dt.timestamp():.0f}" for dt in dt_range]

    styledata = {}

    for country in gdf.index:
        pdf = pd.DataFrame(
            {
                "color": np.random.normal(size=n_periods),
                "opacity": np.random.normal(size=n_periods),
            },
            index=dt_index,
        )
        styledata[country] = pdf.cumsum()

    max_color, min_color = 0, 0

    for country, data in styledata.items():
        max_color = max(max_color, data["color"].max())
        min_color = min(max_color, data["color"].min())

    cmap = linear.PuRd_09.scale(min_color, max_color)

    # Define function to normalize column into range [0,1]
    def norm(col):
        return (col - col.min()) / (col.max() - col.min())

    for country, data in styledata.items():
        data["color"] = data["color"].apply(cmap)
        data["opacity"] = norm(data["opacity"])

    styledict = {
        str(country): data.to_dict(orient="index")
        for country, data in styledata.items()
    }

    m = folium.Map((0, 0), tiles="Stamen Watercolor", zoom_start=2)

    time_slider_choropleth = TimeSliderChoropleth(gdf.to_json(), styledict)
    time_slider_choropleth.add_to(m)

    rendered = time_slider_choropleth._template.module.script(time_slider_choropleth)

    m._repr_html_()
    out = normalize(m._parent.render())
    assert '<script src="https://d3js.org/d3.v4.min.js"></script>' in out

    # We verify that data has been inserted correctly
    expected_timestamps = sorted(dt_index, key=int)  # numeric sort
    expected_timestamps = f"var timestamps = {expected_timestamps};"
    expected_timestamps = expected_timestamps.split(";")[0].strip().replace("'", '"')
    rendered_timestamps = rendered.split(";")[0].strip()
    assert expected_timestamps == rendered_timestamps

    expected_styledict = normalize(json.dumps(styledict, sort_keys=True))
    assert expected_styledict in normalize(rendered)
