## Tiles

### Built-in tilesets

```{code-cell} ipython3
import folium


lon, lat = -38.625, -12.875

zoom_start = 8
```

```{code-cell} ipython3
folium.Map(location=[lat, lon], tiles="OpenStreetMap", zoom_start=zoom_start)
```

```{code-cell} ipython3
folium.Map(location=[lat, lon], tiles="Cartodb Positron", zoom_start=zoom_start)
```

```{code-cell} ipython3
folium.Map(location=[lat, lon], tiles="Cartodb dark_matter", zoom_start=zoom_start)
```


### Custom tiles

You can also provide a url template to load tiles from, for example if you use a paid API.
You also have to provide an attribution in that case. For information how that
url template should look like see the Leaflet documentation:
https://leafletjs.com/reference.html#tilelayer.

Below is an example, note the literal `{z}`, `{x}` and `{y}` in the url template.

```{code-cell} ipython3
attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
)
tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"

folium.Map(location=[lat, lon], tiles=tiles, attr=attr, zoom_start=zoom_start)
```

### Other tilesets

For a list of many more tile providers go to https://leaflet-extras.github.io/leaflet-providers/preview/.

You can also use the xyzservices package: https://github.com/geopandas/xyzservices.
