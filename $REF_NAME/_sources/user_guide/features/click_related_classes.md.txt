```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

### Click-related classes

#### ClickForMarker

`ClickForMarker` lets you create markers on each click.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForMarker()
)
```

*Click on the map to see the effects*

You can customize the popup by providing a string, an IFrame object or an Html object. You can include the latitude and longitude of the marker by using `${lat}` and `${lng}`.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")
)
```

*Click on the map to see the effects*


#### LatLngPopup

`LatLngPopup` lets you create a simple popup at each click.

```{code-cell} ipython3
folium.Map().add_child(
    folium.LatLngPopup()
)
```

*Click on the map to see the effects*

+++

#### ClickForLatLng

`ClickForLatLng` lets you copy coordinates to your browser clipboard.

```{code-cell} ipython3
folium.Map().add_child(
    folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True)
)
```

*Click on the map to see the effects*

If you want to collect back the information in python, you may (install and) import the [clipboard](https://github.com/terryyin/clipboard) library:

```
>>> import clipboard
>>> clipboard.paste()
[-43.580391,-123.824467]
```
