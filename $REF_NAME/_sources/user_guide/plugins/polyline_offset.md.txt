```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

# PolylineOffset

## Basic Demo

- The dashed line is the "model", with no offset applied.
- The Red line is with a -5px offset,
- The Green line is with a 10px offset.
The three are distinct Polyline objects but uses the same coordinate array

```{code-cell} ipython3
m = folium.Map(location=[58.0, -11.0], zoom_start=4, tiles="cartodbpositron")

coords = [
    [58.44773, -28.65234],
    [53, -23.33496],
    [53, -14.32617],
    [58.1707, -10.37109],
    [59, -13],
    [57, -15],
    [57, -18],
    [60, -18],
    [63, -5],
    [59, -7],
    [58, -3],
    [56, -3],
    [60, -4],
]

folium.plugins.PolyLineOffset(
    coords, weight=2, dash_array="5,10", color="black", opacity=1
).add_to(m)

folium.plugins.PolyLineOffset(coords, color="#f00", opacity=1, offset=-5).add_to(m)

folium.plugins.PolyLineOffset(coords, color="#080", opacity=1, offset=10).add_to(m)

m
```

## Bus Lines

A more complex demo.
Offsets are computed automatically depending on the number of bus lines using the same segment.
Other non-offset polylines are used to achieve the white and black outline effect.

```{code-cell} ipython3
m = folium.Map(location=[48.868, 2.365], zoom_start=15)

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"lines": [0, 1]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.357919216156006, 48.87621773324153],
                    [2.357339859008789, 48.874834693731664],
                    [2.362983226776123, 48.86855408432749],
                    [2.362382411956787, 48.86796126699168],
                    [2.3633265495300293, 48.86735432768131],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [2, 3]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.351503372192383, 48.86443950493823],
                    [2.361609935760498, 48.866775611250205],
                    [2.3633265495300293, 48.86735432768131],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [1, 2]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.369627058506012, 48.86619159489603],
                    [2.3724031448364253, 48.8626397112042],
                    [2.3728322982788086, 48.8616233285001],
                    [2.372767925262451, 48.86080456075567],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [0]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.3647427558898926, 48.86653565369396],
                    [2.3647642135620117, 48.86630981023694],
                    [2.3666739463806152, 48.86314789481612],
                    [2.3673176765441895, 48.86066339254944],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [0, 1, 2, 3]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.3633265495300293, 48.86735432768131],
                    [2.3647427558898926, 48.86653565369396],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [1, 2, 3]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.3647427558898926, 48.86653565369396],
                    [2.3650002479553223, 48.86660622956524],
                    [2.365509867668152, 48.866987337550164],
                    [2.369627058506012, 48.86619159489603],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"lines": [3]},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [2.369627058506012, 48.86619159489603],
                    [2.372349500656128, 48.865702850895744],
                ],
            },
        },
    ],
}

# manage overlays in groups to ease superposition order
outlines = folium.FeatureGroup("outlines")
line_bg = folium.FeatureGroup("lineBg")
bus_lines = folium.FeatureGroup("busLines")
bus_stops = folium.FeatureGroup("busStops")

line_weight = 6
line_colors = ["red", "#08f", "#0c0", "#f80"]
stops = []
for line_segment in geojson["features"]:
    # Get every bus line coordinates
    segment_coords = [[x[1], x[0]] for x in line_segment["geometry"]["coordinates"]]
    # Get bus stops coordinates
    stops.append(segment_coords[0])
    stops.append(segment_coords[-1])
    # Get number of bus lines sharing the same coordinates
    lines_on_segment = line_segment["properties"]["lines"]
    # Width of segment proportional to the number of bus lines
    segment_width = len(lines_on_segment) * (line_weight + 1)
    # For the white and black outline effect
    folium.PolyLine(
        segment_coords, color="#000", weight=segment_width + 5, opacity=1
    ).add_to(outlines)
    folium.PolyLine(
        segment_coords, color="#fff", weight=segment_width + 3, opacity=1
    ).add_to(line_bg)
    # Draw parallel bus lines with different color and offset
    for j, line_number in enumerate(lines_on_segment):
        folium.plugins.PolyLineOffset(
            segment_coords,
            color=line_colors[line_number],
            weight=line_weight,
            opacity=1,
            offset=j * (line_weight + 1) - (segment_width / 2) + ((line_weight + 1) / 2),
        ).add_to(bus_lines)

# Draw bus stops
for stop in stops:
    folium.CircleMarker(
        stop,
        color="#000",
        fill_color="#ccc",
        fill_opacity=1,
        radius=10,
        weight=4,
        opacity=1,
    ).add_to(bus_stops)

outlines.add_to(m)
line_bg.add_to(m)
bus_lines.add_to(m)
bus_stops.add_to(m)

m
```
