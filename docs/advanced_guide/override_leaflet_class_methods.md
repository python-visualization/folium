# Overriding Leaflet class methods

```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

## Customizing Leaflet behavior
Sometimes you want to override Leaflet's javascript behavior. This can be done using the `Class.include` statement. This mimics Leaflet's
`L.Class.include` method. See [here](https://leafletjs.com/examples/extending/extending-1-classes.html) for more details.

### Example: adding an authentication header to a TileLayer
One such use case is if you need to override the `createTile` on `L.TileLayer`, because your tiles are hosted on an oauth2 protected
server. This can be done like this:

```{code-cell}
create_tile = folium.JsCode("""
    function(coords, done) {
        const url = this.getTileUrl(coords);
        const img = document.createElement('img');
        fetch(url, {
          headers: {
            "Authorization": "Bearer <Token>"
          },
        })
        .then((response) => {
            img.src = URL.createObjectURL(response.body);
            done(null, img);
        })
        return img;
    }
""")

folium.TileLayer.include(create_tile=create_tile)
tiles = folium.TileLayer(
    tiles="OpenStreetMap",
)
m = folium.Map(
    tiles=tiles,
)


m = folium.Map()
```
