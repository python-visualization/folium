```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# PolyLine

```{code-cell} ipython3
# Coordinates are 15 points on the great circle from Boston to San Francisco.
coordinates = [
    [42.3581, -71.0636],
    [42.82995815, -74.78991444],
    [43.17929819, -78.56603306],
    [43.40320216, -82.37774519],
    [43.49975489, -86.20965845],
    [43.46811941, -90.04569087],
    [43.30857071, -93.86961818],
    [43.02248456, -97.66563267],
    [42.61228259, -101.41886832],
    [42.08133868, -105.11585198],
    [41.4338549, -108.74485069],
    [40.67471747, -112.29609954],
    [39.8093434, -115.76190821],
    [38.84352776, -119.13665678],
    [37.7833, -122.4167],
]

# Create the map and add the line
m = folium.Map(location=[41.9, -97.3], zoom_start=4)

folium.PolyLine(
    locations=coordinates,
    color="#FF0000",
    weight=5,
    tooltip="From Boston to San Francisco",
).add_to(m)

m
```

## Smoothing

PolyLine objects in Leaflet are smoothed by default. This removes points from
the line, putting less load on the browser when drawing. The level of smoothing
can be set with the `smooth_factor` argument.

```{code-cell} ipython3
m = folium.Map(location=[41.9, -97.3], zoom_start=4)

folium.PolyLine(
    smooth_factor=50,
    locations=coordinates,
    color="grey",
    tooltip="Too much smoothing?",
    weight=5,
).add_to(m)

m
```

## Crossing the date line

Take notice how lines behave when they cross the date line.

```{code-cell} ipython3
lon = lat = 0
zoom_start = 1

m = folium.Map(location=[lat, lon], zoom_start=zoom_start)

kw = {"opacity": 1.0, "weight": 6}
folium.PolyLine(
    locations=[(2, 179), (2, -179)],
    tooltip="Wrong",
    color="red",
    line_cap="round",
    **kw,
).add_to(m)

folium.PolyLine(
    locations=[(-2, 179), (-2, 181)],
    tooltip="Correct",
    line_cap="butt",
    color="blue",
    **kw,
).add_to(m)

folium.PolyLine(
    locations=[(-6, -179), (-6, 179)],
    line_cap="square",
    color="green",
    tooltip="Correct",
    **kw,
).add_to(m)

folium.PolyLine(
    locations=[(12, -179), (12, 190)],
    color="orange",
    tooltip="Artifact?",
    **kw,
).add_to(m)

m
```

## Multi-PolyLine

You can create multiple polylines by passing multiple sets of coordinates
to a single `PolyLine` object.

```{code-cell} ipython3
lat = +38.89399
lon = -77.03659
zoom_start = 17

m = folium.Map(location=[lat, lon], zoom_start=zoom_start)

kw = {"color": "red", "fill": True, "radius": 20}

folium.CircleMarker([38.89415, -77.03738], **kw).add_to(m)
folium.CircleMarker([38.89415, -77.03578], **kw).add_to(m)


locations = [
    [
        (38.893596444352134, -77.03814983367920),
        (38.893379333722040, -77.03792452812195),
    ],
    [
        (38.893379333722040, -77.03792452812195),
        (38.893162222428310, -77.03761339187622),
    ],
    [
        (38.893162222428310, -77.03761339187622),
        (38.893028615148424, -77.03731298446655),
    ],
    [
        (38.893028615148424, -77.03731298446655),
        (38.892920059048464, -77.03691601753235),
    ],
    [
        (38.892920059048464, -77.03691601753235),
        (38.892903358095296, -77.03637957572937),
    ],
    [
        (38.892903358095296, -77.03637957572937),
        (38.893011914220770, -77.03592896461487),
    ],
    [
        (38.893011914220770, -77.03592896461487),
        (38.893162222428310, -77.03549981117249),
    ],
    [
        (38.893162222428310, -77.03549981117249),
        (38.893404384982480, -77.03514575958252),
    ],
    [
        (38.893404384982480, -77.03514575958252),
        (38.893596444352134, -77.03496336936950),
    ],
]

folium.PolyLine(
    locations=locations,
    color="orange",
    weight=8,
    opacity=1,
    smooth_factor=0,
).add_to(m)

m
```
