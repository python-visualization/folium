# FloatImage

```{code-cell} ipython3
import folium
from folium.plugins import FloatImage


url = (
    "https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/"
    "a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png"
)

m = folium.Map([-13, -38.15], zoom_start=10)

FloatImage(url, bottom=40, left=65).add_to(m)

m
```
