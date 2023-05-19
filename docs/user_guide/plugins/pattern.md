```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# Pattern plugins

We have two pattern plugin classes: `StripePattern` and `CirclePattern`.

```{code-cell} ipython3
m = folium.Map([40.0, -105.0], zoom_start=6)

url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
stripes = folium.plugins.pattern.StripePattern(angle=-45).add_to(m)

circles = folium.plugins.pattern.CirclePattern(
    width=20, height=20, radius=5, fill_opacity=0.5, opacity=1
).add_to(m)


def style_function(feature):
    default_style = {
        "opacity": 1.0,
        "fillColor": "#ffff00",
        "color": "black",
        "weight": 2,
    }

    if feature["properties"]["name"] == "Colorado":
        default_style["fillPattern"] = stripes
        default_style["fillOpacity"] = 1.0

    if feature["properties"]["name"] == "Utah":
        default_style["fillPattern"] = circles
        default_style["fillOpacity"] = 1.0

    return default_style


# Adding remote GeoJSON as additional layer.
folium.GeoJson(url, smooth_factor=0.5, style_function=style_function).add_to(m)

m
```
