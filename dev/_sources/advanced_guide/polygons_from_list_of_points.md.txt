# Creating a polygon from a list of points

For many of those working with geo data it is a common task being asked to create a polygon from a list of points. More specific, to create a polygon that wraps around those points in a meaningful manner. So, there are several sources in the web explaining how to create the shape (see sources at end of document). This example notebook is the application of those solutions to folium maps.

## Helpers

```{code-cell} ipython3
# Imports
import random

import folium
from scipy.spatial import ConvexHull


# Function to create a list of some random points
def randome_points(amount, LON_min, LON_max, LAT_min, LAT_max):

    points = []
    for _ in range(amount):
        points.append(
            (random.uniform(LON_min, LON_max), random.uniform(LAT_min, LAT_max))
        )

    return points


# Function to draw points in the map
def draw_points(map_object, list_of_points, layer_name, line_color, fill_color, text):

    fg = folium.FeatureGroup(name=layer_name)

    for point in list_of_points:
        fg.add_child(
            folium.CircleMarker(
                point,
                radius=1,
                color=line_color,
                fill_color=fill_color,
                popup=(folium.Popup(text)),
            )
        )

    map_object.add_child(fg)
```

## Convex hull

The convex hull is probably the most common approach - its goal is to create the smallest polygon that contains all points from a given list. The scipy.spatial package provides this algorithm (https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.spatial.ConvexHull.html, accessed 29.12.2018).

```{code-cell} ipython3
# Function that takes a map and a list of points (LON,LAT tuples) and
# returns a map with the convex hull polygon from the points as a new layer


def create_convexhull_polygon(
    map_object, list_of_points, layer_name, line_color, fill_color, weight, text
):

    # Since it is pointless to draw a convex hull polygon around less than 3 points check len of input
    if len(list_of_points) < 3:
        return

    # Create the convex hull using scipy.spatial
    form = [list_of_points[i] for i in ConvexHull(list_of_points).vertices]

    # Create feature group, add the polygon and add the feature group to the map
    fg = folium.FeatureGroup(name=layer_name)
    fg.add_child(
        folium.vector_layers.Polygon(
            locations=form,
            color=line_color,
            fill_color=fill_color,
            weight=weight,
            popup=(folium.Popup(text)),
        )
    )
    map_object.add_child(fg)

    return map_object
```

```{code-cell} ipython3
# Initialize map
my_convexhull_map = folium.Map(location=[48.5, 9.5], zoom_start=8)

# Create a convex hull polygon that contains some points
list_of_points = randome_points(
    amount=10, LON_min=48, LON_max=49, LAT_min=9, LAT_max=10
)

create_convexhull_polygon(
    my_convexhull_map,
    list_of_points,
    layer_name="Example convex hull",
    line_color="lightblue",
    fill_color="lightskyblue",
    weight=5,
    text="Example convex hull",
)

draw_points(
    my_convexhull_map,
    list_of_points,
    layer_name="Example points for convex hull",
    line_color="royalblue",
    fill_color="royalblue",
    text="Example point for convex hull",
)

# Add layer control and show map
folium.LayerControl(collapsed=False).add_to(my_convexhull_map)
my_convexhull_map
```

## Envelope

The envelope is another interesting approach - its goal is to create a box that contains all points from a given list.

```{code-cell} ipython3
def create_envelope_polygon(
    map_object, list_of_points, layer_name, line_color, fill_color, weight, text
):

    # Since it is pointless to draw a box around less than 2 points check len of input
    if len(list_of_points) < 2:
        return

    # Find the edges of box
    from operator import itemgetter

    list_of_points = sorted(list_of_points, key=itemgetter(0))
    x_min = list_of_points[0]
    x_max = list_of_points[len(list_of_points) - 1]

    list_of_points = sorted(list_of_points, key=itemgetter(1))
    y_min = list_of_points[0]
    y_max = list_of_points[len(list_of_points) - 1]

    upper_left = (x_min[0], y_max[1])
    upper_right = (x_max[0], y_max[1])
    lower_right = (x_max[0], y_min[1])
    lower_left = (x_min[0], y_min[1])

    edges = [upper_left, upper_right, lower_right, lower_left]

    # Create feature group, add the polygon and add the feature group to the map
    fg = folium.FeatureGroup(name=layer_name)
    fg.add_child(
        folium.vector_layers.Polygon(
            locations=edges,
            color=line_color,
            fill_color=fill_color,
            weight=weight,
            popup=(folium.Popup(text)),
        )
    )
    map_object.add_child(fg)

    return map_object
```

```{code-cell} ipython3
# Initialize map
my_envelope_map = folium.Map(location=[49.5, 8.5], zoom_start=8)

# Create an envelope polygon that contains some points
list_of_points = randome_points(
    amount=10, LON_min=49.1, LON_max=50, LAT_min=8, LAT_max=9
)

create_envelope_polygon(
    my_envelope_map,
    list_of_points,
    layer_name="Example envelope",
    line_color="indianred",
    fill_color="red",
    weight=5,
    text="Example envelope",
)

draw_points(
    my_envelope_map,
    list_of_points,
    layer_name="Example points for envelope",
    line_color="darkred",
    fill_color="darkred",
    text="Example point for envelope",
)

# Add layer control and show map
folium.LayerControl(collapsed=False).add_to(my_envelope_map)
my_envelope_map
```

## Concave hull (alpha shape)
In some cases the convex hull does not yield good results - this is when the shape of the polygon should be concave instead of convex. The solution is a concave hull that is also called alpha shape. Yet, there is no ready to go, off the shelve solution for this but there are great resources (see: https://web.archive.org/web/20191207074940/http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/, accessed 04.01.2019.


## Putting it together

Just putting it all together...

```{code-cell} ipython3
# Initialize map
my_map_global = folium.Map(location=[48.2460683, 9.26764125], zoom_start=7)

# Create a convex hull polygon that contains some points
list_of_points = randome_points(
    amount=10, LON_min=48, LON_max=49, LAT_min=9, LAT_max=10
)

create_convexhull_polygon(
    my_map_global,
    list_of_points,
    layer_name="Example convex hull",
    line_color="lightblue",
    fill_color="lightskyblue",
    weight=5,
    text="Example convex hull",
)

draw_points(
    my_map_global,
    list_of_points,
    layer_name="Example points for convex hull",
    line_color="royalblue",
    fill_color="royalblue",
    text="Example point for convex hull",
)

# Create an envelope polygon that contains some points
list_of_points = randome_points(
    amount=10, LON_min=49.1, LON_max=50, LAT_min=8, LAT_max=9
)

create_envelope_polygon(
    my_map_global,
    list_of_points,
    layer_name="Example envelope",
    line_color="indianred",
    fill_color="red",
    weight=5,
    text="Example envelope",
)

draw_points(
    my_map_global,
    list_of_points,
    layer_name="Example points for envelope",
    line_color="darkred",
    fill_color="darkred",
    text="Example point for envelope",
)

# Add layer control and show map
folium.LayerControl(collapsed=False).add_to(my_map_global)
my_map_global
```

## Sources:

* https://web.archive.org/web/20200222150431/http://blog.yhat.com/posts/interactive-geospatial-analysis.html, accessed 28.12.2018

* https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.spatial.ConvexHull.html, accessed 29.12.2018

* https://web.archive.org/web/20191207074940/http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/, accessed 04.01.2019
