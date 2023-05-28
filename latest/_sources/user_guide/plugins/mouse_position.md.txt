# MousePosition

This plugin adds a small field to your map that shows the coordinates of your mouse position.
By default it is in the bottom right corner.

```{code-cell} ipython3
import folium
from folium.plugins import MousePosition


m = folium.Map()

MousePosition().add_to(m)

m
```

## Options

```{code-cell} ipython3
m = folium.Map()

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};"

MousePosition(
    position="topright",
    separator=" | ",
    empty_string="NaN",
    lng_first=True,
    num_digits=20,
    prefix="Coordinates:",
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(m)

m
```
