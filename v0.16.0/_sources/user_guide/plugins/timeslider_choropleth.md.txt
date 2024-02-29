# TimeSliderChoropleth

In this example we'll make a choropleth with a timeslider.

The class needs at least two arguments to be instantiated.

1. A string-serielized geojson containing all the features (i.e., the areas)
2. A dictionary with the following structure:

```
styledict = {
    '0': {
        '2017-1-1': {'color': 'ffffff', 'opacity': 1},
        '2017-1-2': {'color': 'fffff0', 'opacity': 1},
        ...
        },
    ...,
    'n': {
        '2017-1-1': {'color': 'ffffff', 'opacity': 1},
        '2017-1-2': {'color': 'fffff0', 'opacity': 1},
        ...
        }
}
```

In the above dictionary, the keys are the feature-ids.

Using both color and opacity gives us the ability to simultaneously visualize two features on the choropleth. I typically use color to visualize the main feature (like, average height) and opacity to visualize how many measurements were in that group.

## Loading the features

We use `geopandas` to load a dataset containing the boundaries of all the countries in the world.

```{code-cell} ipython3
import geopandas as gpd

assert "naturalearth_lowres" in gpd.datasets.available
datapath = gpd.datasets.get_path("naturalearth_lowres")
gdf = gpd.read_file(datapath)
```

```{code-cell} ipython3
%matplotlib inline

ax = gdf.plot(figsize=(10, 10))
```

The `GeoDataFrame` contains the boundary coordinates, as well as some other data such as estimated population.

```{code-cell} ipython3
gdf.head()
```

## Creating the style dictionary

Now we generate time series data for each country.

Data for different areas might be sampled at different times, and `TimeSliderChoropleth` can deal with that. This means that there is no need to resample the data, as long as the number of datapoints isn't too large for the browser to deal with.

To simulate that data is sampled at different times we random sample data for `n_periods` rows of data and then pick without replacing `n_sample` of those rows.

```{code-cell} ipython3
import pandas as pd

n_periods, n_sample = 48, 40

assert n_sample < n_periods

datetime_index = pd.date_range("2016-1-1", periods=n_periods, freq="M")
dt_index_epochs = datetime_index.astype("int64") // 10 ** 9
dt_index = dt_index_epochs.astype("U10")

dt_index
```

```{code-cell} ipython3
import numpy as np

styledata = {}

for country in gdf.index:
    df = pd.DataFrame(
        {
            "color": np.random.normal(size=n_periods),
            "opacity": np.random.normal(size=n_periods),
        },
        index=dt_index,
    )
    df = df.cumsum()
    df.sample(n_sample, replace=False).sort_index()
    styledata[country] = df
```

Note that the geodata and random sampled data is linked through the feature_id, which is the index of the `GeoDataFrame`.

```{code-cell} ipython3
gdf.loc[0]
```

```{code-cell} ipython3
styledata.get(0).head()
```

We see that we generated two series of data for each country; one for color and one for opacity. Let's plot them to see what they look like.

```{code-cell} ipython3
ax = df.plot()
```

Looks random alright. We want to map the column named `color` to a hex color. To do this we use a normal colormap. To create the colormap, we calculate the maximum and minimum values over all the timeseries. We also need the max/min of the `opacity` column, so that we can map that column into a range [0,1].

```{code-cell} ipython3
max_color, min_color, max_opacity, min_opacity = 0, 0, 0, 0

for country, data in styledata.items():
    max_color = max(max_color, data["color"].max())
    min_color = min(max_color, data["color"].min())
    max_opacity = max(max_color, data["opacity"].max())
    max_opacity = min(max_color, data["opacity"].max())
```

Define and apply colormaps:

```{code-cell} ipython3
from branca.colormap import linear

cmap = linear.PuRd_09.scale(min_color, max_color)


def norm(x):
    return (x - x.min()) / (x.max() - x.min())


for country, data in styledata.items():
    data["color"] = data["color"].apply(cmap)
    data["opacity"] = norm(data["opacity"])
```

```{code-cell} ipython3
styledata.get(0).head()
```

Finally we use `pd.DataFrame.to_dict()` to convert each dataframe into a dictionary, and place each of these in a map from country id to data.

```{code-cell} ipython3
styledict = {
    str(country): data.to_dict(orient="index") for country, data in styledata.items()
}
```

## Creating the map

```{code-cell} ipython3
import folium
from folium.plugins import TimeSliderChoropleth


m = folium.Map([0, 0], zoom_start=2)

TimeSliderChoropleth(
    gdf.to_json(),
    styledict=styledict,
).add_to(m)

m
```

### Initial timestamp

By default the timeslider starts at the beginning. You can also select another timestamp to begin with using the `init_timestamp` parameter. Note that it expects an index to the list of timestamps. In this example we use `-1` to select the last timestamp.

```{code-cell} ipython3
m = folium.Map([0, 0], zoom_start=2)

TimeSliderChoropleth(
    gdf.to_json(),
    styledict=styledict,
    init_timestamp=-1,
).add_to(m)

m
```
