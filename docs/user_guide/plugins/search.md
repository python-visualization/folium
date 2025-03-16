# Search

The `Search` plugin allows you to search in your `GeoJson`, `TopoJson`, `FeatureGroup` or `MarkerCluster` objects.

## Search in GeoJSON

### Data

Let's get some JSON data from the web - both a point layer and a polygon GeoJson dataset with some population data.

```{code-cell} ipython3
import geopandas

states = geopandas.read_file(
    "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json",
    driver="GeoJSON",
)

cities = geopandas.read_file(
    "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_populated_places_simple.geojson",
    driver="GeoJSON",
)
```

And take a look at what our data looks like:

```{code-cell} ipython3
states.describe()
```

Look how far the minimum and maximum values for the density are from the top and bottom quartile breakpoints! We have some outliers in our data that are well outside the meat of most of the distribution. Let's look into this to find the culprits within the sample.

```{code-cell} ipython3
import pandas as pd

states_sorted = states.sort_values(by="density", ascending=False)

pd.concat([
    states_sorted.nlargest(5, 'density')[['name', 'density']],
    states_sorted.nsmallest(5, 'density')[['name', 'density']]
])
```

Looks like Washington D.C. and Alaska were the culprits on each end of the range. Washington was more dense than the next most dense state, New Jersey, than the least dense state, Alaska was from Wyoming, however. Washington D.C. has a has a relatively small land area for the amount of people that live there, so it makes sense that it's pretty dense. And Alaska has a lot of land area, but not much of it is habitable for humans.


However, we're looking at all of the states in the US to look at things on a more regional level. That high figure at the top of our range for Washington D.C. will really hinder the ability for us to differentiate between the other states, so let's account for that in the min and max values for our color scale, by getting the quantile values close to the end of the range. Anything higher or lower than those values will just fall into the 'highest' and 'lowest' bins for coloring.

```{code-cell} ipython3
def rd2(x):
    return round(x, 2)

minimum, maximum = states["density"].quantile([0.05, 0.95]).apply(rd2)

mean = round(states["density"].mean(), 2)

print(f"minimum: {minimum}", f"maximum: {maximum}", f"Mean: {mean}", sep="\n\n")
```

This looks better. Our min and max values for the colorscale are much closer to the mean value now. Let's run with these values, and make a colorscale. I'm just going to use a sequential light-to-dark color palette from the [ColorBrewer](https://colorbrewer2.org/?type=sequential&scheme=Purples&n=5).

```{code-cell} ipython3
import branca


colormap = branca.colormap.LinearColormap(
    colors=["#f2f0f7", "#cbc9e2", "#9e9ac8", "#756bb1", "#54278f"],
    index=states["density"].quantile([0.2, 0.4, 0.6, 0.8]),
    vmin=minimum,
    vmax=maximum,
)

colormap.caption = "Population Density in the United States"

colormap
```

Let's narrow down these cities to United states cities, by using GeoPandas' spatial join functionality between two GeoDataFrame objects, using the Point 'within' Polygon functionality.

```{code-cell} ipython3
us_cities = geopandas.sjoin(cities, states, how="inner", predicate="within")

pop_ranked_cities = us_cities.sort_values(by="pop_max", ascending=False)[
    ["nameascii", "pop_max", "geometry"]
].iloc[:20]
```

Ok, now we have a new GeoDataFrame with our top 20 populated cities. Let's see the top 5.

```{code-cell} ipython3
pop_ranked_cities.head(5)
```

### Map with Search plugin and GeoJSON data

Alright, let's build a map!

```{code-cell} ipython3
import folium
from folium.plugins import Search


m = folium.Map(location=[38, -97], zoom_start=4)


def style_function(x):
    return {
        "fillColor": colormap(x["properties"]["density"]),
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    }


stategeo = folium.GeoJson(
    states,
    name="US States",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "density"], aliases=["State", "Density"], localize=True
    ),
).add_to(m)

citygeo = folium.GeoJson(
    pop_ranked_cities,
    name="US Cities",
    tooltip=folium.GeoJsonTooltip(
        fields=["nameascii", "pop_max"], aliases=["", "Population Max"], localize=True
    ),
).add_to(m)

statesearch = Search(
    layer=stategeo,
    geom_type="Polygon",
    placeholder="Search for a US State",
    collapsed=False,
    search_label="name",
    weight=3,
).add_to(m)

citysearch = Search(
    layer=citygeo,
    geom_type="Point",
    placeholder="Search for a US City",
    collapsed=True,
    search_label="nameascii",
).add_to(m)

folium.LayerControl().add_to(m)
colormap.add_to(m)

m
```

## Search in FeatureGroup

Here's an example how to search `Marker`s in a `FeatureGroup`. Note how we
add an extra field to each `Marker` that is then used to search on.


```{code-cell} ipython3
from folium import Map, FeatureGroup, Marker, Icon
from folium.plugins import Search

m = Map((45.5236, -122.5), tiles="carto db positron")

fg = FeatureGroup().add_to(m)
Marker([45.5236, -122.7], icon=Icon(color="red"), title="red").add_to(fg)
Marker([45.5236, -122.5], icon=Icon(color="blue"), title="blue").add_to(fg)
Marker([45.5236, -122.3], icon=Icon(color="green"), title="green").add_to(fg)

Search(fg, search_label="title").add_to(m)

m
```
