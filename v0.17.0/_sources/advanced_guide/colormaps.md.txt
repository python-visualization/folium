```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Using colormaps

A few examples of how to use `folium.colormap` in choropleths.

Let's load a GeoJSON file, and try to choropleth it.

```{code-cell} ipython3
import pandas
import requests

geo_json_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
unemployment = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)

unemployment_dict = unemployment.set_index("State")["Unemployment"]
```

## Self-defined

You can build a choropleth in using a self-defined function.
It has to output an hexadecimal color string of the form `#RRGGBB` or `#RRGGBBAA`.

```{code-cell} ipython3
def my_color_function(feature):
    """Maps low values to green and high values to red."""
    if unemployment_dict[feature["id"]] > 6.5:
        return "#ff0000"
    else:
        return "#008000"
```

```{code-cell} ipython3
m = folium.Map([43, -100], tiles="cartodbpositron", zoom_start=4)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        "fillColor": my_color_function(feature),
        "color": "black",
        "weight": 2,
        "dashArray": "5, 5",
    },
).add_to(m)

m
```

## StepColormap

But to help you define your colormap, we've embedded `StepColormap` in `folium.colormap`.

You can simply define the colors you want, and the `index` (*thresholds*) that correspond.

```{code-cell} ipython3
import branca.colormap as cm

step = cm.StepColormap(
    ["green", "yellow", "red"], vmin=3, vmax=10, index=[3, 4, 8, 10], caption="step"
)

step
```

```{code-cell} ipython3
m = folium.Map([43, -100], tiles="cartodbpositron", zoom_start=4)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        "fillColor": step(unemployment_dict[feature["id"]]),
        "color": "black",
        "weight": 2,
        "dashArray": "5, 5",
    },
).add_to(m)

m
```

If you specify no index, colors will be set uniformly.

```{code-cell} ipython3
cm.StepColormap(["r", "y", "g", "c", "b", "m"])
```

## LinearColormap

But sometimes, you would prefer to have a *continuous* set of colors. This can be done by `LinearColormap`.

```{code-cell} ipython3
linear = cm.LinearColormap(["green", "yellow", "red"], vmin=3, vmax=10)

linear
```

```{code-cell} ipython3
m = folium.Map([43, -100], tiles="cartodbpositron", zoom_start=4)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        "fillColor": linear(unemployment_dict[feature["id"]]),
        "color": "black",
        "weight": 2,
        "dashArray": "5, 5",
    },
).add_to(m)

m
```

Again, you can set the `index` if you want something irregular.

```{code-cell} ipython3
cm.LinearColormap(["red", "orange", "yellow", "green"], index=[0, 0.1, 0.9, 1.0])
```

If you want to transform a linear map into a *step* one, you can use the method `to_step`.

```{code-cell} ipython3
linear.to_step(6)
```

You can also use more sophisticated rules to create the thresholds.

```{code-cell} ipython3
linear.to_step(
    n=6,
    data=[30.6, 50, 51, 52, 53, 54, 55, 60, 70, 100],
    method="quantiles",
    round_method="int",
)
```

And the opposite is also possible with `to_linear`.

```{code-cell} ipython3
step.to_linear()
```

## Built-in

For convenience, we provide a (small) set of built-in linear colormaps, in `folium.colormap.linear`.

```{code-cell} ipython3
cm.linear.OrRd_09
```

You can also use them to generate regular `StepColormap`.

```{code-cell} ipython3
cm.linear.PuBuGn_09.to_step(12)
```

Of course, you may need to scale the colormaps to your bounds. This is doable with `.scale`.

```{code-cell} ipython3
cm.linear.YlGnBu_09.scale(3, 12)
```

```{code-cell} ipython3
cm.linear.RdGy_11.to_step(10).scale(5, 100)
```

At last, if you want to check them all, simply ask for `linear` in the notebook.

```{code-cell} ipython3
cm.linear
```

## Draw a `ColorMap` on a map

By the way, a ColorMap is also a Folium `Element` that you can draw on a map.

```{code-cell} ipython3
m = folium.Map(tiles="cartodbpositron")

colormap = cm.linear.Set1_09.scale(0, 35).to_step(10)
colormap.caption = "A colormap caption"
m.add_child(colormap)

m
```
