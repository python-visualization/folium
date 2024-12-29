```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# GeoJSON point features with markers


```{code-cell} ipython3
import geopandas

gdf = geopandas.read_file(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson"
)

gdf.head()
```

```{code-cell} ipython3
gdf['href'] = '<a href="' + gdf.url + '">' + gdf.url + "</a>"
gdf['service_level'] = gdf.notes.str.split(', ').apply(lambda x: len([v for v in x if "all" in v]))
gdf['lines_served'] = gdf.line.str.split('-').apply(lambda x: len(x))
```

```{code-cell} ipython3
service_levels = gdf.service_level.unique().tolist()
service_levels
```

```{code-cell} ipython3
colors = ["orange", "yellow", "green", "blue"]
```

## Use a Circle as a Marker

```{code-cell} ipython3
m = folium.Map(location=[40.75, -73.95], zoom_start=13)

folium.GeoJson(
    gdf,
    name="Subway Stations",
    marker=folium.Circle(radius=4, fill_color="orange", fill_opacity=0.4, color="black", weight=1),
    tooltip=folium.GeoJsonTooltip(fields=["name", "line", "notes"]),
    popup=folium.GeoJsonPopup(fields=["name", "line", "href", "notes"]),
    style_function=lambda x: {
        "fillColor": colors[x['properties']['service_level']],
        "radius": (x['properties']['lines_served'])*30,
    },
    highlight_function=lambda x: {"fillOpacity": 0.8},
    zoom_on_click=True,
).add_to(m)

m
```

## Or use a DivIcon

```{code-cell} ipython3
m = folium.Map(location=[40.75, -73.95], zoom_start=13)


def style_function(feature):
    props = feature.get('properties')
    markup = f"""
        <a href="{props.get('url')}">
            <div style="font-size: 0.8em;">
            <div style="width: 10px;
                        height: 10px;
                        border: 1px solid black;
                        border-radius: 5px;
                        background-color: orange;">
            </div>
            {props.get('name')}
        </div>
        </a>
    """
    return {"html": markup}


folium.GeoJson(
    gdf,
    name="Subway Stations",
    marker=folium.Marker(icon=folium.DivIcon()),
    tooltip=folium.GeoJsonTooltip(fields=["name", "line", "notes"]),
    popup=folium.GeoJsonPopup(fields=["name", "line", "href", "notes"]),
    style_function=style_function,
    zoom_on_click=True,
).add_to(m)

m
```

## Use a Marker

```{code-cell} ipython3
m = folium.Map(location=[40.75, -73.95], zoom_start=13)

marker_colors = ["red", "orange", "green", "blue"]

folium.GeoJson(
    gdf,
    name="Subway Stations",
    zoom_on_click=True,
    marker=folium.Marker(icon=folium.Icon(icon='star')),
    tooltip=folium.GeoJsonTooltip(fields=["name", "line", "notes"]),
    popup=folium.GeoJsonPopup(fields=["name", "line", "href", "notes"]),
    style_function=lambda x: {
        'markerColor': marker_colors[x['properties']['service_level']],
    },
).add_to(m)

m
```
