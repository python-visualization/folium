```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Using `Choropleth`

Now if you want to get faster, you can use the `Choropleth` class. Have a look at it's docstring, it has several styling options.

Just like the `GeoJson` class you can provide it a filename, a dict, or a geopandas object.

```{code-cell} ipython3
import requests

m = folium.Map([43, -100], zoom_start=4)

us_states = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

folium.Choropleth(
    geo_data=us_states,
    fill_opacity=0.3,
    line_weight=2,
).add_to(m)

m
```

Then, in playing with keyword arguments, you can get a choropleth in a few lines:

```{code-cell} ipython3
import pandas

state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)

m = folium.Map([43, -100], zoom_start=4)

folium.Choropleth(
    geo_data=us_states,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
).add_to(m)

m
```

You can force the color scale to a given number of bins (or directly list the bins you would like), by providing the `bins` argument.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4)

folium.Choropleth(
    geo_data=us_states,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    bins=[3, 4, 9, 11],
).add_to(m)

m
```

You can also enable the highlight function, to enable highlight functionality when you hover over each area.

```{code-cell} ipython3
m = folium.Map(location=[48, -102], zoom_start=3)
folium.Choropleth(
    geo_data=us_states,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
    highlight=True,
).add_to(m)

m
```

You can customize the way missing and `nan` values are displayed on your map using the two parameters `nan_fill_color` and `nan_fill_opacity`.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4)

messed_up_data = state_data.drop(0)
messed_up_data.loc[4, "Unemployment"] = float("nan")

folium.Choropleth(
    geo_data=us_states,
    data=messed_up_data,
    columns=["State", "Unemployment"],
    nan_fill_color="purple",
    nan_fill_opacity=0.4,
    key_on="feature.id",
    fill_color="YlGn",
).add_to(m)

m
```

Internally Choropleth uses the `GeoJson` or `TopoJson` class, depending on your settings, and the `StepColormap` class. Both objects are attributes of your `Choropleth` object called `geojson` and `color_scale`. You can make changes to them, but for regular things you won't have to. For example setting a name for in the layer controls or disabling showing the layer on opening the map is possible in `Choropleth` itself.

```{code-cell} ipython3
m = folium.Map([43, -100], zoom_start=4)

choropleth = folium.Choropleth(
    geo_data=us_states,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    name="Unenployment",
    show=False,
).add_to(m)

# The underlying GeoJson and StepColormap objects are reachable
print(type(choropleth.geojson))
print(type(choropleth.color_scale))

folium.LayerControl(collapsed=False).add_to(m)

m
```
