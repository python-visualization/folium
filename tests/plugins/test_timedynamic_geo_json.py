"""
tests for folium.plugins.TimeDynamicGeoJson
"""
import json
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from branca.colormap import linear

def test_timedynamic_geo_json():
    """
    tests folium.plugins.TimeDynamicGeoJson
    """
    assert 'naturalearth_lowres' in gpd.datasets.available
    datapath = gpd.datasets.get_path('naturalearth_lowres')
    gdf = gpd.read_file(datapath)

    n_periods = 10
    dt_index = pd.date_range('2016-1-1', periods=n_periods, freq='M').strftime('%s')

    styledata = {}

    for country in gdf.index:
        pdf = pd.DataFrame({'color': np.random.normal(size=n_periods),
                            'opacity': np.random.normal(size=n_periods)},
                            index=dt_index)
        styledata[country] = pdf.cumsum()

    max_color, min_color = 0, 0

    for country, data in styledata.items():
        max_color = max(max_color, data['color'].max())
        min_color = min(max_color, data['color'].min())

    cmap = linear.PuRd.scale(min_color, max_color)
    norm = lambda x: (x - x.min())/(x.max()-x.min())

    for country, data in styledata.items():
        data['color'] = data['color'].apply(cmap)
        data['opacity'] = norm(data['opacity'])

    styledict = {str(country): data.to_dict(orient='index') for
                 country, data in styledata.items()}

    m = folium.Map((0, 0), tiles='Stamen Watercolor', zoom_start=2)

    folium.plugins.TimeDynamicGeoJson(
        gdf.to_json(),
        styledict
    ).add_to(m)

    m.save('testmap.html')
    m._repr_html_()

    out = m._parent.render()

    # We verify that imports
    assert '<script src="https://d3js.org/d3.v4.min.js' in out  # noqa

    # We verify that data has been inserted currectly
    expected_timestamps = ("var timestamps = ['1454166000', '1456671600', '1459350000', "
                           "'1461942000', '1464620400', '1467212400', '1469890800', "
                           "'1472569200', '1475161200', '1477839600'];")
    assert expected_timestamps in out

    expected_styledict = json.dumps(styledict).replace('"', "'")
    assert expected_styledict in out
