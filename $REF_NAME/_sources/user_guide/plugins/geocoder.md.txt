```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
import folium.plugins
```

## Geocoder

Add a search box to the map to search for geographic features like cities, countries, etc. You can search with names or addresses.

Uses the Nomatim service from OpenStreetMap. Please respect their usage policy: https://operations.osmfoundation.org/policies/nominatim/

```{code-cell} ipython3
m = folium.Map()

folium.plugins.Geocoder().add_to(m)

m
```
