from typing import Optional, Union

from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer


class VectorGridProtobuf(JSCSSMixin, Layer):
    """
    Add vector tile layers based on https://github.com/Leaflet/Leaflet.VectorGrid.

    Parameters
    ----------
    url: str
        url to tile provider
        e.g. https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}
    name: str, optional
        Name of the layer that will be displayed in LayerControl
    options: dict or str, optional
        VectorGrid.protobuf options, which you can pass as python dictionary or string.
        Strings allow plain JavaScript to be passed, therefore allow for conditional styling (see examples).

        Additionally the url might contain any string literals like {token}, or {key}
        that can be passed as attribute to the options dict and will be substituted.

        Every layer inside the tile layer has to be styled separately.
    overlay : bool, default True
        Whether your layer will be an overlay (ticked with a check box in
        LayerControls) or a base layer (ticked with a radio button).
    control: bool, default True
        Whether the layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.

    Examples
    --------

    Options as dict:

    >>> m = folium.Map()
    >>> url = "https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}"
    >>> options = {
    ...     "subdomain": "tilehosting",
    ...     "token": "af6P2G9dztAt1F75x7KYt0Hx2DJR052G",
    ...     "vectorTileLayerStyles": {
    ...         "layer_name_one": {
    ...             "fill": True,
    ...             "weight": 1,
    ...             "fillColor": "green",
    ...             "color": "black",
    ...             "fillOpacity": 0.6,
    ...             "opacity": 0.6,
    ...         },
    ...         "layer_name_two": {
    ...             "fill": True,
    ...             "weight": 1,
    ...             "fillColor": "red",
    ...             "color": "black",
    ...             "fillOpacity": 0.6,
    ...             "opacity": 0.6,
    ...         },
    ...     },
    ... }

    >>> VectorGridProtobuf(url, "layer_name", options).add_to(m)

    Options as string allows to pass functions

    >>> m = folium.Map()
    >>> url = "https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}"
    >>> options = '''{
    ...     "subdomain": "tilehosting",
    ...     "token": "af6P2G9dztAt1F75x7KYt0Hx2DJR052G",
    ...     "vectorTileLayerStyles": {
    ...         all: function(f) {
    ...             if (f.type === 'parks') {
    ...                 return {
    ...                     "fill": true,
    ...                     "weight": 1,
    ...                     "fillColor": 'green',
    ...                     "color": 'black',
    ...                     "fillOpacity":0.6,
    ...                     "opacity":0.6
    ...                 };
    ...             }
    ...             if (f.type === 'water') {
    ...                 return {
    ...                     "fill": true,
    ...                     "weight": 1,
    ...                     "fillColor": 'purple',
    ...                     "color": 'black',
    ...                     "fillOpacity":0.6,
    ...                     "opacity":0.6
    ...                 };
    ...             }
    ...         }
    ...     }
    ... }'''

    >>> VectorGridProtobuf(url, "layer_name", options).add_to(m)


    For more info, see: https://leaflet.github.io/Leaflet.VectorGrid/vectorgrid-api-docs.html#styling-vectorgrids.
    """

    _template = Template(
        """
            {% macro script(this, kwargs) -%}
            var {{ this.get_name() }} = L.vectorGrid.protobuf(
                '{{ this.url }}',
                {%- if this.options is defined %}
                    {{ this.options if this.options is string else this.options|tojson }}
                {%- endif %}
            );
            {%- endmacro %}
            """
    )

    default_js = [
        (
            "vectorGrid",
            "https://unpkg.com/leaflet.vectorgrid@latest/dist/Leaflet.VectorGrid.bundled.js",
        )
    ]

    def __init__(
        self,
        url: str,
        name: Optional[str] = None,
        options: Union[str, dict, None] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "VectorGridProtobuf"
        self.url = url
        if options is not None:
            self.options = options
