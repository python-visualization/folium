```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## LocateControl

Adds a control button that when clicked, the user device geolocation is displayed.
For list of all possible keyword options see 'Possible options' on https://github.com/domoritz/leaflet-locatecontrol.

To work properly in production, the connection needs to be encrypted (HTTPS),
otherwise the browser will not allow users to share their location.

```{code-cell} ipython3
m = folium.Map([41.97, 2.81])

folium.plugins.LocateControl().add_to(m)

# If you want get the user device position after load the map, set auto_start=True
folium.plugins.LocateControl(auto_start=False).add_to(m)

m
```
