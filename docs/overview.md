Overview
==========

Folium is a geographical visualization library for Python, based on
[Leaflet.js](https://leafletjs.com/).

Here's a basic example of creating a map:

```{code-cell} ipython3
import folium

m = folium.Map(location=[45.5236, -122.6750])
```

If you are in a Jupyter Notebook, you can display it like this:

```{code-cell} ipython3
m
```

Or you can save it as an HTML file:

```{code-cell} ipython3
m.save("index.html")
```
