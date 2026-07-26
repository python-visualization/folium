```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Custom tiles

## No tiles

```{code-cell} ipython3
import requests

states = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

kw = {"location": [48, -102], "zoom_start": 3}
```

```{code-cell} ipython3
m = folium.Map(tiles=None, **kw)

folium.GeoJson(states).add_to(m)

m
```

## Use image as tiles

```{code-cell} ipython3
import branca

# Create a white image of 4 pixels, and embed it in a url.
white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])

# Create a map using this url for each tile.
m = folium.Map(tiles=white_tile, attr="white tile", **kw)

folium.GeoJson(states).add_to(m)

m
```

## Create a larger pattern to use as tiles

```{code-cell} ipython3
images = [[(-1) ** ((i + j) // 30) for i in range(300)] for j in range(300)]

tiles = branca.utilities.image_to_url(images)

m = folium.Map(tiles=tiles, attr="Just because we can", **kw)

folium.GeoJson(states).add_to(m)

m
```

```{code-cell} ipython3
images = [[(-1) ** ((i // 30 + j // 30)) for i in range(300)] for j in range(300)]

tiles = branca.utilities.image_to_url(images)

m = folium.Map(tiles=tiles, attr="Just because we can", **kw)

folium.GeoJson(states).add_to(m)

m
```
