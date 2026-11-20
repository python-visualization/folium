```{code-cell} ipython3
---
nbsphinx: hidden
---
import folium
```

# Show feature info in a fixed box

A `GeoJsonTooltip` follows the mouse. Sometimes you want the information in a
fixed place instead, for example in the top right corner of the map, like the
info box in [Leaflet's interactive choropleth tutorial](https://leafletjs.com/examples/choropleth/).

folium doesn't have a class for this, but you can build one with two small
pieces:

- a Leaflet control that holds the box, and
- an `on_each_feature` callback on the `GeoJson` that updates the box when the
  mouse enters or leaves a feature.

## Prepare the data

We'll show the unemployment rate per US state. We add the rate to the
properties of each GeoJson feature, so the info box can read it from there.

```{code-cell} ipython3
import csv
import io

import requests

base_url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main"
geo_json_data = requests.get(f"{base_url}/us_states.json").json()
unemployment_csv = requests.get(f"{base_url}/us_unemployment_oct_2012.csv").text

unemployment = {
    row["State"]: float(row["Unemployment"])
    for row in csv.DictReader(io.StringIO(unemployment_csv))
}
for feature in geo_json_data["features"]:
    feature["properties"]["unemployment"] = unemployment[feature["id"]]
```

## The info box

The info box is a `MacroElement` that creates a
[Leaflet control](https://leafletjs.com/reference.html#control). The control
gets an `update` method: called with the properties of a feature, it shows the
fields you picked; called without arguments, it shows a placeholder text.

The text is set with `textContent`, so values from your data are never parsed
as HTML.

```{code-cell} ipython3
from branca.element import MacroElement
from jinja2 import Template


class InfoBox(MacroElement):
    """A box at a fixed position on the map that shows feature properties."""

    _template = Template(
        """
        {% macro header(this, kwargs) %}
        <style>
            .info-box {
                padding: 6px 8px;
                font: 14px/16px Arial, Helvetica, sans-serif;
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                border-radius: 5px;
            }
            .info-box h4 { margin: 0 0 5px; color: #777; }
        </style>
        {% endmacro %}

        {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = L.control({position: {{ this.position|tojson }}});

        {{ this.get_name() }}.onAdd = function (map) {
            this._div = L.DomUtil.create("div", "info-box");
            this.update();
            return this._div;
        };

        {{ this.get_name() }}.update = function (props) {
            const fields = {{ this.fields|tojson }};
            const aliases = {{ this.aliases|tojson }};
            this._div.replaceChildren();

            const title = L.DomUtil.create("h4", "", this._div);
            title.textContent = {{ this.title|tojson }};

            if (!props) {
                L.DomUtil.create("span", "", this._div).textContent = {{ this.placeholder|tojson }};
                return;
            }
            fields.forEach(function (field, i) {
                const row = L.DomUtil.create("div", "", this._div);
                L.DomUtil.create("b", "", row).textContent = aliases[i] + " ";
                row.append(String(props[field]));
            }, this);
        };

        {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    def __init__(
        self,
        fields,
        aliases=None,
        title="",
        placeholder="Hover over a feature",
        position="topright",
    ):
        super().__init__()
        self._name = "InfoBox"
        self.fields = list(fields)
        self.aliases = list(aliases) if aliases is not None else self.fields
        self.title = title
        self.placeholder = placeholder
        self.position = position
```

## Connect the box to the GeoJson

The `on_each_feature` callback adds a `mouseover` and a `mouseout` handler to
each feature. Because we pass the info box to `JsCode` as a parameter,
`%(info)s` is replaced by the Javascript name of the box when the map is
rendered.

The `highlight_function` takes care of highlighting the state under the mouse,
as usual.

```{code-cell} ipython3
import branca.colormap as cm

colormap = cm.linear.YlGn_09.scale(
    min(unemployment.values()), max(unemployment.values())
)

m = folium.Map([43, -100], zoom_start=4)

info = InfoBox(
    fields=["name", "unemployment"],
    aliases=["State:", "Unemployment (%):"],
    title="US unemployment, October 2012",
    placeholder="Hover over a state",
).add_to(m)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["unemployment"]),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    highlight_function=lambda feature: {"weight": 3, "fillOpacity": 0.9},
    on_each_feature=folium.JsCode(
        """
        function (feature, layer) {
            layer.on({
                mouseover: function () { %(info)s.update(feature.properties); },
                mouseout: function () { %(info)s.update(); },
            });
        }
        """,
        info=info,
    ),
).add_to(m)

m
```

`position` takes the same values as other Leaflet controls: `"topright"`,
`"topleft"`, `"bottomright"` or `"bottomleft"`.
