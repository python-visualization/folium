# VideoOverlay

```{code-cell} ipython3
import folium


m = folium.Map(location=[22.5, -115], zoom_start=4)

video = folium.raster_layers.VideoOverlay(
    video_url="https://www.mapbox.com/bites/00188/patricia_nasa.webm",
    bounds=[[32, -130], [13, -100]],
    opacity=0.65,
    attr="Video from patricia_nasa",
    autoplay=True,
    loop=False,
)

video.add_to(m)

m
```
