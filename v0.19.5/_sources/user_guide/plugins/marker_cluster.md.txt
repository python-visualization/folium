# MarkerCluster

```{code-cell} ipython3
import folium
from folium.plugins import MarkerCluster

m = folium.Map(location=[44, -73], zoom_start=5)

marker_cluster = MarkerCluster().add_to(m)

folium.Marker(
    location=[40.67, -73.94],
    popup="Add popup text here.",
    icon=folium.Icon(color="green", icon="ok-sign"),
).add_to(marker_cluster)

folium.Marker(
    location=[44.67, -73.94],
    popup="Add popup text here.",
    icon=folium.Icon(color="red", icon="remove-sign"),
).add_to(marker_cluster)

folium.Marker(
    location=[44.67, -71.94],
    popup="Add popup text here.",
    icon=None,
).add_to(marker_cluster)

m
```

```{code-cell} ipython3
import numpy as np

size = 100
lons = np.random.randint(-180, 180, size=size)
lats = np.random.randint(-90, 90, size=size)

locations = list(zip(lats, lons))
popups = ["lon:{}<br>lat:{}".format(lon, lat) for (lat, lon) in locations]
```

## Adding all icons in a single call

```{code-cell} ipython3
icon_create_function = """\
function(cluster) {
    return L.divIcon({
    html: '<b>' + cluster.getChildCount() + '</b>',
    className: 'marker-cluster marker-cluster-large',
    iconSize: new L.Point(20, 20)
    });
}"""
```

```{code-cell} ipython3
from folium.plugins import MarkerCluster

m = folium.Map(
    location=[np.mean(lats), np.mean(lons)], tiles="Cartodb Positron", zoom_start=1
)

marker_cluster = MarkerCluster(
    locations=locations,
    popups=popups,
    name="1000 clustered icons",
    overlay=True,
    control=True,
    icon_create_function=icon_create_function,
)

marker_cluster.add_to(m)

folium.LayerControl().add_to(m)

m
```

## Explicit loop allows for customization in the loop.

```{code-cell} ipython3
m = folium.Map(
    location=[np.mean(lats), np.mean(lons)],
    tiles='Cartodb Positron',
    zoom_start=1
)

marker_cluster = MarkerCluster(
    name='1000 clustered icons',
    overlay=True,
    control=False,
    icon_create_function=None
)

for k in range(size):
    location = lats[k], lons[k]
    marker = folium.Marker(location=location)
    popup = 'lon:{}<br>lat:{}'.format(location[1], location[0])
    folium.Popup(popup).add_to(marker)
    marker_cluster.add_child(marker)

marker_cluster.add_to(m)

folium.LayerControl().add_to(m);

m
```

## FastMarkerCluster

`FastMarkerCluster` is not as flexible as MarkerCluster but, like the name suggests, it is faster.

```{code-cell} ipython3
from folium.plugins import FastMarkerCluster

m = folium.Map(
    location=[np.mean(lats), np.mean(lons)],
    tiles='Cartodb Positron',
    zoom_start=1
)

FastMarkerCluster(data=list(zip(lats, lons))).add_to(m)

folium.LayerControl().add_to(m);

m
```

```{code-cell} ipython3
callback = """\
function (row) {
    var icon, marker;
    icon = L.AwesomeMarkers.icon({
        icon: "map-marker", markerColor: "red"});
    marker = L.marker(new L.LatLng(row[0], row[1]));
    marker.setIcon(icon);
    return marker;
};
"""

m = folium.Map(
    location=[np.mean(lats), np.mean(lons)], tiles="Cartodb Positron", zoom_start=1
)

FastMarkerCluster(data=list(zip(lats, lons)), callback=callback).add_to(m)

m
```
