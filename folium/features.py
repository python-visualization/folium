"""
Leaflet GeoJson and miscellaneous features.

"""

import functools
import json
import operator
import warnings
from collections.abc import Iterable, Sequence
from typing import (
    Any,
    Callable,
    Optional,
    Union,
    get_args,
)

import numpy as np
import requests
from branca.colormap import ColorMap, LinearColormap, StepColormap
from branca.element import (
    Div,
    Element,
    Figure,
    Html,
    IFrame,
    JavascriptLink,
    MacroElement,
)
from branca.utilities import color_brewer

from folium.elements import JSCSSMixin
from folium.folium import Map
from folium.map import Class, FeatureGroup, Icon, Layer, Marker, Popup, Tooltip
from folium.template import Template
from folium.utilities import (
    JsCode,
    TypeBoundsReturn,
    TypeContainer,
    TypeJsonValue,
    TypeLine,
    TypePathOptions,
    TypePosition,
    _parse_size,
    escape_backticks,
    get_bounds,
    get_obj_in_upper_tree,
    image_to_url,
    javascript_identifier_path_to_array_notation,
    none_max,
    none_min,
    remove_empty,
    validate_locations,
)
from folium.vector_layers import Circle, CircleMarker, PolyLine, path_options


class RegularPolygonMarker(JSCSSMixin, Marker):
    """
    Custom markers using the Leaflet Data Vis Framework.

    Parameters
    ----------
    location: tuple or list
        Latitude and Longitude of Marker (Northing, Easting)
    number_of_sides: int, default 4
        Number of polygon sides
    rotation: int, default 0
        Rotation angle in degrees
    radius: int, default 15
        Marker radius, in pixels
    popup: string or Popup, optional
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, optional
        Display a text when hovering over the object.
    **kwargs:
        See vector layers path_options for additional arguments.

    https://humangeo.github.io/leaflet-dvf/

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = new L.RegularPolygonMarker(
                {{ this.location|tojson }},
                {{ this.options|tojavascript }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    default_js = [
        (
            "dvf_js",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.3.0/leaflet-dvf.markers.min.js",
        ),
    ]

    def __init__(
        self,
        location: Sequence[float],
        number_of_sides: int = 4,
        rotation: int = 0,
        radius: int = 15,
        popup: Union[Popup, str, None] = None,
        tooltip: Union[Tooltip, str, None] = None,
        **kwargs: TypePathOptions,
    ):
        super().__init__(location, popup=popup, tooltip=tooltip)
        self._name = "RegularPolygonMarker"
        self.options = path_options(line=False, radius=radius, **kwargs)
        self.options.update(
            dict(
                number_of_sides=number_of_sides,
                rotation=rotation,
            )
        )


class Vega(JSCSSMixin):
    """
    Creates a Vega chart element.

    Parameters
    ----------
    data: JSON-like str or object
        The Vega description of the chart.
        It can also be any object that has a method `to_json`,
        so that you can (for instance) provide a `vincent` chart.
    width: int or str, default None
        The width of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    height: int or str, default None
        The height of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    left: int or str, default '0%'
        The horizontal distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    top: int or str, default '0%'
        The vertical distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    position: str, default 'relative'
        The `position` argument that the CSS shall contain.
        Ex: 'relative', 'absolute'

    """

    _template = Template("")

    default_js = [
        ("d3", "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"),
        ("vega", "https://cdnjs.cloudflare.com/ajax/libs/vega/1.4.3/vega.min.js"),
        ("jquery", "https://code.jquery.com/jquery-3.7.1.min.js"),
    ]

    def __init__(
        self,
        data: Any,
        width: Union[int, str, None] = None,
        height: Union[int, str, None] = None,
        left: Union[int, str] = "0%",
        top: Union[int, str] = "0%",
        position: str = "relative",
    ):
        super().__init__()
        self._name = "Vega"
        self.data = data.to_json() if hasattr(data, "to_json") else data
        if isinstance(self.data, str):
            self.data = json.loads(self.data)

        # Size Parameters.
        self.width = _parse_size(
            self.data.get("width", "100%") if width is None else width
        )
        self.height = _parse_size(
            self.data.get("height", "100%") if height is None else height
        )
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        super().render(**kwargs)

        self.json = json.dumps(self.data)

        self._parent.html.add_child(
            Element(
                Template(
                    """
            <div id="{{this.get_name()}}"></div>
            """
                ).render(this=self, kwargs=kwargs)
            ),
            name=self.get_name(),
        )

        self._parent.script.add_child(
            Element(
                Template(
                    """
            vega_parse({{this.json}},{{this.get_name()}});
            """
                ).render(this=self)
            ),
            name=self.get_name(),
        )

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        figure.header.add_child(
            Element(
                Template(
                    """
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
            """
                ).render(this=self, **kwargs)
            ),
            name=self.get_name(),
        )

        figure.script.add_child(
            Template(
                """function vega_parse(spec, div) {
            vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });}"""
            ),  # noqa
            name="vega_parse",
        )


class VegaLite(MacroElement):
    """
    Creates a Vega-Lite chart element.

    Parameters
    ----------
    data: JSON-like str or object
        The Vega-Lite description of the chart.
        It can also be any object that has a method `to_json`,
        so that you can (for instance) provide an `Altair` chart.
    width: int or str, default None
        The width of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    height: int or str, default None
        The height of the output element.
        If None, either data['width'] (if available) or '100%' will be used.
        Ex: 120, '120px', '80%'
    left: int or str, default '0%'
        The horizontal distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    top: int or str, default '0%'
        The vertical distance of the output with respect to the parent
        HTML object. Ex: 120, '120px', '80%'
    position: str, default 'relative'
        The `position` argument that the CSS shall contain.
        Ex: 'relative', 'absolute'

    """

    _template = Template("")

    def __init__(
        self,
        data: Any,
        width: Union[int, str, None] = None,
        height: Union[int, str, None] = None,
        left: Union[int, str] = "0%",
        top: Union[int, str] = "0%",
        position: str = "relative",
    ):
        super(self.__class__, self).__init__()
        self._name = "VegaLite"
        self.data = data.to_json() if hasattr(data, "to_json") else data
        if isinstance(self.data, str):
            self.data = json.loads(self.data)

        self.json = json.dumps(self.data)

        # Size Parameters.
        self.width = _parse_size(
            self.data.get("width", "100%") if width is None else width
        )
        self.height = _parse_size(
            self.data.get("height", "100%") if height is None else height
        )
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        parent = self._parent
        if not isinstance(parent, (Figure, Div, Popup)):
            raise TypeError(
                "VegaLite elements can only be added to a Figure, Div, or Popup"
            )

        parent.html.add_child(
            Element(
                Template(
                    """
            <div id="{{this.get_name()}}"></div>
            """
                ).render(this=self, kwargs=kwargs)
            ),
            name=self.get_name(),
        )

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        figure.header.add_child(
            Element(
                Template(
                    """
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
            """
                ).render(this=self, **kwargs)
            ),
            name=self.get_name(),
        )

        embed_mapping = {
            1: self._embed_vegalite_v1,
            2: self._embed_vegalite_v2,
            3: self._embed_vegalite_v3,
            4: self._embed_vegalite_v4,
            5: self._embed_vegalite_v5,
        }

        # Version 2 is assumed as the default, if no version is given in the schema.
        embed_vegalite = embed_mapping.get(
            self.vegalite_major_version, self._embed_vegalite_v2
        )
        embed_vegalite(figure=figure, parent=parent)

    @property
    def vegalite_major_version(self) -> Optional[int]:
        if "$schema" not in self.data:
            return None

        schema = self.data["$schema"]

        return int(schema.split("/")[-1].split(".")[0].lstrip("v"))

    def _embed_vegalite_v5(self, figure: Figure, parent: TypeContainer) -> None:
        self._vega_embed(parent=parent)

        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm//vega@5"), name="vega"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@5"), name="vega-lite"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@6"),
            name="vega-embed",
        )

    def _embed_vegalite_v4(self, figure: Figure, parent: TypeContainer) -> None:
        self._vega_embed(parent=parent)

        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm//vega@5"), name="vega"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@4"), name="vega-lite"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@6"),
            name="vega-embed",
        )

    def _embed_vegalite_v3(self, figure: Figure, parent: TypeContainer) -> None:
        self._vega_embed(parent=parent)

        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega@4"), name="vega"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@3"), name="vega-lite"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@3"),
            name="vega-embed",
        )

    def _embed_vegalite_v2(self, figure: Figure, parent: TypeContainer) -> None:
        self._vega_embed(parent=parent)

        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega@3"), name="vega"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@2"), name="vega-lite"
        )
        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@3"),
            name="vega-embed",
        )

    def _vega_embed(self, parent: TypeContainer) -> None:
        parent.script.add_child(
            Element(
                Template(
                    """
                    vegaEmbed({{this.get_name()}}, {{this.json}})
                        .then(function(result) {})
                        .catch(console.error);
                """
                ).render(this=self)
            ),
            name=self.get_name(),
        )

    def _embed_vegalite_v1(self, figure: Figure, parent: TypeContainer) -> None:
        parent.script.add_child(
            Element(
                Template(
                    """
                    var embedSpec = {
                        mode: "vega-lite",
                        spec: {{this.json}}
                    };
                    vg.embed(
                        {{this.get_name()}}, embedSpec, function(error, result) {}
                    );
                """
                ).render(this=self)
            ),
            name=self.get_name(),
        )

        figure.header.add_child(
            JavascriptLink("https://d3js.org/d3.v3.min.js"), name="d3"
        )
        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/vega/2.6.5/vega.js"),
            name="vega",
        )
        figure.header.add_child(
            JavascriptLink(
                "https://cdnjs.cloudflare.com/ajax/libs/vega-lite/1.3.1/vega-lite.js"
            ),
            name="vega-lite",
        )
        figure.header.add_child(
            JavascriptLink(
                "https://cdnjs.cloudflare.com/ajax/libs/vega-embed/2.2.0/vega-embed.js"
            ),
            name="vega-embed",
        )


class GeoJson(Layer):
    """
    Creates a GeoJson object for plotting into a Map.

    Parameters
    ----------
    data: file, dict or str.
        The GeoJSON data you want to plot.
        * If file, then data will be read in the file and fully
        embedded in Leaflet's JavaScript.
        * If dict, then data will be converted to JSON and embedded
        in the JavaScript.
        * If str, then data will be passed to the JavaScript as-is.
        * If `__geo_interface__` is available, the `__geo_interface__`
        dictionary will be serialized to JSON and
        reprojected if `to_crs` is available.

    style_function: function, default None
        Function mapping a GeoJson Feature to a style dict.
    highlight_function: function, default None
        Function mapping a GeoJson Feature to a style dict for mouse events.
    popup_keep_highlighted: bool, default False
        Whether to keep the highlighting active while the popup is open
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls
    show: bool, default True
        Whether the layer will be shown on opening.
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    tooltip: GeoJsonTooltip, Tooltip or str, default None
        Display a text when hovering over the object. Can utilize the data,
        see folium.GeoJsonTooltip for info on how to do that.
    popup: GeoJsonPopup, optional
        Show a different popup for each feature by passing a GeoJsonPopup object.
    marker: Circle, CircleMarker or Marker, optional
        If your data contains Point geometry, you can format the markers by passing a Circle,
        CircleMarker or Marker object with your wanted options. The `style_function` and
        `highlight_function` will also target the marker object you passed.
    embed: bool, default True
        Whether to embed the data in the html file or not. Note that disabling
        embedding is only supported if you provide a file link or URL.
    zoom_on_click: bool, default False
        Set to True to enable zooming in on a geometry when clicking on it.
    on_each_feature: JsCode, optional
        Javascript code to be called on each feature.
        See https://leafletjs.com/examples/geojson/
        `onEachFeature` for more information.
    **kwargs
        Keyword arguments are passed to the geoJson object as extra options.

    Examples
    --------
    >>> # Providing filename that shall be embedded.
    >>> GeoJson("foo.json")
    >>> # Providing filename that shall not be embedded.
    >>> GeoJson("foo.json", embed=False)
    >>> # Providing dict.
    >>> GeoJson(json.load(open("foo.json")))
    >>> # Providing string.
    >>> GeoJson(open("foo.json").read())

    >>> # Provide a style_function that color all states green but Alabama.
    >>> style_function = lambda x: {
    ...     "fillColor": (
    ...         "#0000ff" if x["properties"]["name"] == "Alabama" else "#00ff00"
    ...     )
    ... }
    >>> GeoJson(geojson, style_function=style_function)

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        {%- if this.style %}
        function {{ this.get_name() }}_styler(feature) {
            switch({{ this.feature_identifier }}) {
                {%- for style, ids_list in this.style_map.items() if not style == 'default' %}
                {% for id_val in ids_list %}case {{ id_val|tojson }}: {% endfor %}
                    return {{ style }};
                {%- endfor %}
                default:
                    return {{ this.style_map['default'] }};
            }
        }
        {%- endif %}
        {%- if this.highlight %}
        function {{ this.get_name() }}_highlighter(feature) {
            switch({{ this.feature_identifier }}) {
                {%- for style, ids_list in this.highlight_map.items() if not style == 'default' %}
                {% for id_val in ids_list %}case {{ id_val|tojson }}: {% endfor %}
                    return {{ style }};
                {%- endfor %}
                default:
                    return {{ this.highlight_map['default'] }};
            }
        }
        {%- endif %}

        {%- if this.marker %}
        function {{ this.get_name() }}_pointToLayer(feature, latlng) {
            var opts = {{ this.marker.options | tojavascript }};
            {% if this.marker._name == 'Marker' and this.marker.icon %}
            const iconOptions = {{ this.marker.icon.options | tojavascript }}
            const iconRootAlias = L{%- if this.marker.icon._name == "Icon" %}.AwesomeMarkers{%- endif %}
            opts.icon = new iconRootAlias.{{ this.marker.icon._name }}(iconOptions)
            {% endif %}
            {%- if this.style_function %}
            let style = {{ this.get_name()}}_styler(feature)
            Object.assign({%- if this.marker.icon -%}opts.icon.options{%- else -%} opts {%- endif -%}, style)
            {% endif %}
            return new L.{{this.marker._name}}(latlng, opts)
        }
        {%- endif %}

        function {{this.get_name()}}_onEachFeature(feature, layer) {
            {%- if this.on_each_feature %}
            ({{this.on_each_feature}})(feature, layer);
            {%- endif %}

            layer.on({
                {%- if this.highlight %}
                mouseout: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        {%- if this.popup_keep_highlighted %}
                        if (!e.target.isPopupOpen())
                        {%- endif %}
                            {{ this.get_name() }}.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = {{ this.get_name() }}_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
                {%- if this.popup_keep_highlighted %}
                popupopen: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        const highlightStyle = {{ this.get_name() }}_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                        e.target.bindPopup(e.popup)
                    }
                },
                popupclose: function(e) {
                    if(typeof e.target.setStyle === "function"){
                        {{ this.get_name() }}.resetStyle(e.target);
                        e.target.unbindPopup()
                    }
                },
                {%- endif %}
                {%- endif %}
                {%- if this.zoom_on_click %}
                click: function(e) {
                    if (typeof e.target.getBounds === 'function') {
                        {{ this.parent_map.get_name() }}.fitBounds(e.target.getBounds());
                    }
                    else if (typeof e.target.getLatLng === 'function'){
                        let zoom = {{ this.parent_map.get_name() }}.getZoom()
                        zoom = zoom > 12 ? zoom : zoom + 1
                        {{ this.parent_map.get_name() }}.flyTo(e.target.getLatLng(), zoom)
                    }
                }
                {%- endif %}
            });
        };
        var {{ this.get_name() }} = L.geoJson(null, {
            {%- if this.smooth_factor is not none  %}
                smoothFactor: {{ this.smooth_factor|tojson }},
            {%- endif %}
                onEachFeature: {{ this.get_name() }}_onEachFeature,
            {% if this.style %}
                style: {{ this.get_name() }}_styler,
            {%- endif %}
            {%- if this.marker %}
                pointToLayer: {{ this.get_name() }}_pointToLayer,
            {%- endif %}
            ...{{this.options | tojavascript }}
        });

        function {{ this.get_name() }}_add (data) {
            {{ this.get_name() }}
                .addData(data);
        }
        {%- if this.embed %}
            {{ this.get_name() }}_add({{ this.data|tojson }});
        {%- else %}
            $.ajax({{ this.embed_link|tojson }}, {dataType: 'json', async: false})
                .done({{ this.get_name() }}_add);
        {%- endif %}

        {%- if not this.style %}
        {{this.get_name()}}.setStyle(function(feature) {return feature.properties.style;});
        {%- endif %}

        {% endmacro %}
        """
    )  # noqa

    def __init__(
        self,
        data: Any,
        style_function: Optional[Callable] = None,
        highlight_function: Optional[Callable] = None,
        popup_keep_highlighted: bool = False,
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        smooth_factor: Optional[float] = None,
        tooltip: Union[str, Tooltip, "GeoJsonTooltip", None] = None,
        embed: bool = True,
        popup: Optional["GeoJsonPopup"] = None,
        zoom_on_click: bool = False,
        on_each_feature: Optional[JsCode] = None,
        marker: Union[Circle, CircleMarker, Marker, None] = None,
        **kwargs: Any,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "GeoJson"
        self.embed = embed
        self.embed_link: Optional[str] = None
        self.json = None
        self.parent_map = None
        self.smooth_factor = smooth_factor
        self.style = style_function is not None
        self.highlight = highlight_function is not None
        self.zoom_on_click = zoom_on_click
        if marker:
            if not isinstance(marker, (Circle, CircleMarker, Marker)):
                raise TypeError(
                    "Only Marker, Circle, and CircleMarker are supported as GeoJson marker types."
                )

        if popup_keep_highlighted and popup is None:
            raise ValueError(
                "A popup is needed to use the popup_keep_highlighted feature"
            )
        self.popup_keep_highlighted = popup_keep_highlighted

        self.marker = marker
        self.on_each_feature = on_each_feature
        self.options = remove_empty(**kwargs)

        self.data = self.process_data(data)

        if self.style or self.highlight:
            self.convert_to_feature_collection()
            if style_function is not None:
                self._validate_function(style_function, "style_function")
                self.style_function = style_function
                self.style_map: dict = {}
            if highlight_function is not None:
                self._validate_function(highlight_function, "highlight_function")
                self.highlight_function = highlight_function
                self.highlight_map: dict = {}
            self.feature_identifier = self.find_identifier()

        if isinstance(tooltip, (GeoJsonTooltip, Tooltip)):
            self.add_child(tooltip)
        elif tooltip is not None:
            self.add_child(Tooltip(tooltip))
        if isinstance(popup, (GeoJsonPopup, Popup)):
            self.add_child(popup)

    def process_data(self, data: Any) -> dict:
        """Convert an unknown data input into a geojson dictionary."""
        if isinstance(data, dict):
            self.embed = True
            return data
        elif isinstance(data, str):
            if data.lower().startswith(("http:", "ftp:", "https:")):
                if not self.embed:
                    self.embed_link = data
                return self.get_geojson_from_web(data)
            elif data.lstrip()[0] in "[{":  # This is a GeoJSON inline string
                self.embed = True
                return json.loads(data)
            else:  # This is a filename
                if not self.embed:
                    self.embed_link = data
                with open(data) as f:
                    return json.loads(f.read())
        elif hasattr(data, "__geo_interface__"):
            self.embed = True
            if hasattr(data, "to_crs"):
                data = data.to_crs("EPSG:4326")
            return json.loads(json.dumps(data.__geo_interface__))
        else:
            raise ValueError(
                "Cannot render objects with any missing geometries" f": {data!r}"
            )

    def get_geojson_from_web(self, url: str) -> dict:
        return requests.get(url).json()

    def convert_to_feature_collection(self) -> None:
        """Convert data into a FeatureCollection if it is not already."""
        if self.data["type"] == "FeatureCollection":
            return
        if not self.embed:
            raise ValueError(
                "Data is not a FeatureCollection, but it should be to apply "
                "style or highlight. Because `embed=False` it cannot be "
                "converted into one.\nEither change your geojson data to a "
                "FeatureCollection, set `embed=True` or disable styling."
            )
        # Catch case when GeoJSON is just a single Feature or a geometry.
        if "geometry" not in self.data.keys():
            # Catch case when GeoJSON is just a geometry.
            self.data = {"type": "Feature", "geometry": self.data}
        self.data = {"type": "FeatureCollection", "features": [self.data]}

    def _validate_function(self, func: Callable, name: str) -> None:
        """
        Tests `self.style_function` and `self.highlight_function` to ensure
        they are functions returning dictionaries.
        """
        # If for some reason there are no features (e.g., empty API response)
        # don't attempt validation
        if not self.data["features"]:
            return

        test_feature = self.data["features"][0]
        if not callable(func) or not isinstance(func(test_feature), dict):
            raise ValueError(
                f"{name} should be a function that accepts items from "
                "data['features'] and returns a dictionary."
            )

    def find_identifier(self) -> str:
        """Find a unique identifier for each feature, create it if needed.

        According to the GeoJSON specs a feature:
         - MAY have an 'id' field with a string or numerical value.
         - MUST have a 'properties' field. The content can be any json object
           or even null.

        """
        feats = self.data["features"]
        # Each feature has an 'id' field with a unique value.
        unique_ids = {feat.get("id", None) for feat in feats}
        if None not in unique_ids and len(unique_ids) == len(feats):
            return "feature.id"
        # Each feature has a unique string or int property.
        if all(isinstance(feat.get("properties", None), dict) for feat in feats):
            for key in feats[0]["properties"]:
                unique_values = {
                    feat["properties"].get(key, None)
                    for feat in feats
                    if isinstance(feat["properties"].get(key, None), (str, int))
                }
                if len(unique_values) == len(feats):
                    return f"feature.properties.{key}"
        # We add an 'id' field with a unique value to the data.
        if self.embed:
            for i, feature in enumerate(feats):
                feature["id"] = str(i)
            return "feature.id"
        raise ValueError(
            "There is no unique identifier for each feature and because "
            "`embed=False` it cannot be added. Consider adding an `id` "
            "field to your geojson data or set `embed=True`. "
        )

    def _get_self_bounds(self) -> list[list[Optional[float]]]:
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return get_bounds(self.data, lonlat=True)

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        # Need at least one feature, otherwise style mapping fails
        if (self.style or self.highlight) and self.data["features"]:
            mapper = GeoJsonStyleMapper(self.data, self.feature_identifier, self)
            if self.style:
                self.style_map = mapper.get_style_map(self.style_function)
            if self.highlight:
                self.highlight_map = mapper.get_highlight_map(self.highlight_function)
        super().render()


TypeStyleMapping = dict[str, Union[str, list[Union[str, int]]]]


class GeoJsonStyleMapper:
    """Create dicts that map styling to GeoJson features.

    :meta private:
    """

    def __init__(
        self,
        data: dict,
        feature_identifier: str,
        geojson_obj: GeoJson,
    ):
        self.data = data
        self.feature_identifier = feature_identifier
        self.geojson_obj = geojson_obj

    def get_style_map(self, style_function: Callable) -> TypeStyleMapping:
        """Return a dict that maps style parameters to features."""
        return self._create_mapping(style_function, "style")

    def get_highlight_map(self, highlight_function: Callable) -> TypeStyleMapping:
        """Return a dict that maps highlight parameters to features."""
        return self._create_mapping(highlight_function, "highlight")

    def _create_mapping(self, func: Callable, switch: str) -> TypeStyleMapping:
        """Internal function to create the mapping."""
        mapping: TypeStyleMapping = {}
        for feature in self.data["features"]:
            content = func(feature)
            if switch == "style":
                for key, value in content.items():
                    if isinstance(value, MacroElement):
                        # Make sure objects are rendered:
                        if value._parent is None:
                            value._parent = self.geojson_obj
                            value.render()
                        # Replace objects with their Javascript var names:
                        content[key] = "{{'" + value.get_name() + "'}}"
            key = self._to_key(content)
            feature_id = self.get_feature_id(feature)
            mapping.setdefault(key, []).append(feature_id)  # type: ignore
        self._set_default_key(mapping)
        return mapping

    def get_feature_id(self, feature: dict) -> Union[str, int]:
        """Return a value identifying the feature."""
        fields = self.feature_identifier.split(".")[1:]
        value = functools.reduce(operator.getitem, fields, feature)
        assert isinstance(value, (str, int))
        return value

    @staticmethod
    def _to_key(d: dict) -> str:
        """Convert dict to str and enable Jinja2 template syntax."""
        as_str = json.dumps(d, sort_keys=True)
        return as_str.replace('"{{', "{{").replace('}}"', "}}")

    @staticmethod
    def _set_default_key(mapping: TypeStyleMapping) -> None:
        """Replace the field with the most features with a 'default' field."""
        key_longest = max(mapping, key=mapping.get)  # type: ignore
        mapping["default"] = key_longest
        del mapping[key_longest]


class TopoJson(JSCSSMixin, Layer):
    """
    Creates a TopoJson object for plotting into a Map.

    Parameters
    ----------
    data: file, dict or str.
        The TopoJSON data you want to plot.
        * If file, then data will be read in the file and fully
        embedded in Leaflet's JavaScript.
        * If dict, then data will be converted to JSON and embedded
        in the JavaScript.
        * If str, then data will be passed to the JavaScript as-is.

    object_path: str
        The path of the desired object into the TopoJson structure.
        Ex: 'objects.myobject'.
    style_function: function, default None
        A function mapping a TopoJson geometry to a style dict.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    tooltip: GeoJsonTooltip, Tooltip or str, default None
        Display a text when hovering over the object. Can utilize the data,
        see folium.GeoJsonTooltip for info on how to do that.

    Examples
    --------
    >>> # Providing file that shall be embedded.
    >>> TopoJson(open("foo.json"), "object.myobject")
    >>> # Providing filename that shall not be embedded.
    >>> TopoJson("foo.json", "object.myobject")
    >>> # Providing dict.
    >>> TopoJson(json.load(open("foo.json")), "object.myobject")
    >>> # Providing string.
    >>> TopoJson(open("foo.json").read(), "object.myobject")

    >>> # Provide a style_function that color all states green but Alabama.
    >>> style_function = lambda x: {
    ...     "fillColor": (
    ...         "#0000ff" if x["properties"]["name"] == "Alabama" else "#00ff00"
    ...     )
    ... }
    >>> TopoJson(topo_json, "object.myobject", style_function=style_function)

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }}_data = {{ this.data|tojson }};
            var {{ this.get_name() }} = L.geoJson(
                topojson.feature(
                    {{ this.get_name() }}_data,
                    {{ this.get_name() }}_data{{ this._safe_object_path }}
                ),
                {
                {%- if this.smooth_factor is not none %}
                    smoothFactor: {{ this.smooth_factor|tojson }},
                {%- endif %}
                }
            ).addTo({{ this._parent.get_name() }});
            {{ this.get_name() }}.setStyle(function(feature) {
                return feature.properties.style;
            });
        {% endmacro %}
        """
    )  # noqa

    default_js = [
        (
            "topojson",
            "https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js",
        ),
    ]

    def __init__(
        self,
        data: Any,
        object_path: str,
        style_function: Optional[Callable] = None,
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        smooth_factor: Optional[float] = None,
        tooltip: Union[str, Tooltip, None] = None,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "TopoJson"

        if "read" in dir(data):
            self.embed = True
            self.data = json.load(data)
        elif type(data) is dict:
            self.embed = True
            self.data = data
        else:
            self.embed = False
            self.data = data

        self.object_path = object_path
        self._safe_object_path = javascript_identifier_path_to_array_notation(
            object_path
        )

        self.style_function = style_function or (lambda x: {})

        self.smooth_factor = smooth_factor

        if isinstance(tooltip, (GeoJsonTooltip, Tooltip)):
            self.add_child(tooltip)
        elif tooltip is not None:
            self.add_child(Tooltip(tooltip))

    def style_data(self) -> None:
        """Applies self.style_function to each feature of self.data."""

        def recursive_get(data, keys):
            if len(keys):
                return recursive_get(data.get(keys[0]), keys[1:])
            else:
                return data

        geometries = recursive_get(self.data, self.object_path.split("."))[
            "geometries"
        ]  # noqa
        for feature in geometries:
            feature.setdefault("properties", {}).setdefault("style", {}).update(
                self.style_function(feature)
            )  # noqa

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        self.style_data()
        super().render(**kwargs)

    def get_bounds(self) -> TypeBoundsReturn:
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        if not self.embed:
            raise ValueError("Cannot compute bounds of non-embedded TopoJSON.")

        xmin, xmax, ymin, ymax = None, None, None, None

        for arc in self.data["arcs"]:
            x, y = 0, 0
            for dx, dy in arc:
                x += dx
                y += dy
                xmin = none_min(x, xmin)
                xmax = none_max(x, xmax)
                ymin = none_min(y, ymin)
                ymax = none_max(y, ymax)
        return [
            [
                self.data["transform"]["translate"][1]
                + self.data["transform"]["scale"][1] * ymin,  # noqa
                self.data["transform"]["translate"][0]
                + self.data["transform"]["scale"][0] * xmin,  # noqa
            ],
            [
                self.data["transform"]["translate"][1]
                + self.data["transform"]["scale"][1] * ymax,  # noqa
                self.data["transform"]["translate"][0]
                + self.data["transform"]["scale"][0] * xmax,  # noqa
            ],
        ]


class GeoJsonDetail(MacroElement):
    """Base class for GeoJsonTooltip and GeoJsonPopup.

    :meta private:
    """

    base_template = """
    function(layer){
    let div = L.DomUtil.create('div');
    {% if this.fields %}
    let handleObject = feature => {
        if (feature === null) {
            return '';
        } else if (typeof(feature)=='object') {
            return JSON.stringify(feature);
        } else {
            return feature;
        }
    }
    let fields = {{ this.fields | tojson | safe }};
    let aliases = {{ this.aliases | tojson | safe }};
    let table = '<table>' +
        String(
        fields.map(
        (v,i)=>
        `<tr>{% if this.labels %}
            <th>${aliases[i]{% if this.localize %}.toLocaleString(){% endif %}}</th>
            {% endif %}
            <td>${handleObject(layer.feature.properties[v]){% if this.localize %}.toLocaleString(){% endif %}}</td>
        </tr>`).join(''))
    +'</table>';
    div.innerHTML=table;
    {% endif %}
    return div
    }
    """

    def __init__(
        self,
        fields: Sequence[str],
        aliases: Optional[Sequence[str]] = None,
        labels: bool = True,
        localize: bool = False,
        style: Optional[str] = None,
        class_name: str = "geojsondetail",
    ):
        super().__init__()
        assert isinstance(
            fields, (list, tuple)
        ), "Please pass a list or tuple to fields."
        if aliases is not None:
            assert isinstance(aliases, (list, tuple))
            assert len(fields) == len(
                aliases
            ), "fields and aliases must have the same length."
        assert isinstance(labels, bool), "labels requires a boolean value."
        assert isinstance(localize, bool), "localize must be bool."
        self._name = "GeoJsonDetail"
        self.fields = fields
        self.aliases = aliases if aliases is not None else fields
        self.labels = labels
        self.localize = localize
        self.class_name = class_name
        if style:
            assert isinstance(
                style, str
            ), "Pass a valid inline HTML style property string to style."
            # noqa outside of type checking.
            self.style = style

    def warn_for_geometry_collections(self) -> None:
        """Checks for GeoJson GeometryCollection features to warn user about incompatibility."""
        assert isinstance(self._parent, GeoJson)
        geom_collections = [
            feature.get("properties") if feature.get("properties") is not None else key
            for key, feature in enumerate(self._parent.data["features"])
            if feature["geometry"]
            and feature["geometry"]["type"] == "GeometryCollection"
        ]
        if any(geom_collections):
            warnings.warn(
                f"{self._name} is not configured to render for GeoJson GeometryCollection geometries. "
                f"Please consider reworking these features: {geom_collections} to MultiPolygon for full functionality.\n"
                "https://tools.ietf.org/html/rfc7946#page-9",
                UserWarning,
            )

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        figure = self.get_root()
        if isinstance(self._parent, GeoJson):
            keys = tuple(
                self._parent.data["features"][0]["properties"].keys()
                if self._parent.data["features"]
                else []
            )
            self.warn_for_geometry_collections()
        elif isinstance(self._parent, TopoJson):
            obj_name = self._parent.object_path.split(".")[-1]
            keys = tuple(
                self._parent.data["objects"][obj_name]["geometries"][0][
                    "properties"
                ].keys()
            )
        else:
            raise TypeError(
                f"You cannot add a {self._name} to anything other than a "
                "GeoJson or TopoJson object."
            )
        keys = tuple(x for x in keys if x not in ("style", "highlight"))
        for value in self.fields:
            assert (
                value in keys
            ), f"The field {value} is not available in the data. Choose from: {keys}."
        figure.header.add_child(
            Element(
                Template(
                    """
                    <style>
                        .{{ this.class_name }} {
                            {{ this.style }}
                        }
                       .{{ this.class_name }} table{
                            margin: auto;
                        }
                        .{{ this.class_name }} tr{
                            text-align: left;
                        }
                        .{{ this.class_name }} th{
                            padding: 2px; padding-right: 8px;
                        }
                    </style>
            """
                ).render(this=self)
            ),
            name=self.get_name() + "tablestyle",
        )

        super().render()


class GeoJsonTooltip(GeoJsonDetail):
    """
    Create a tooltip that uses data from either geojson or topojson.

    Parameters
    ----------
    fields: list or tuple.
        Labels of GeoJson/TopoJson 'properties' or GeoPandas GeoDataFrame
        columns you'd like to display.
    aliases: list/tuple of strings, same length/order as fields, default None.
        Optional aliases you'd like to display in the tooltip as field name
        instead of the keys of `fields`.
    labels: bool, default True.
        Set to False to disable displaying the field names or aliases.
    localize: bool, default False.
        This will use JavaScript's .toLocaleString() to format 'clean' values
        as strings for the user's location; i.e. 1,000,000.00 comma separators,
        float truncation, etc.
        Available for most of JavaScript's primitive types (any data you'll
        serve into the template).
    style: str, default None.
        HTML inline style properties like font and colors. Will be applied to
        a div with the text in it.
    sticky: bool, default True
        Whether the tooltip should follow the mouse.
    **kwargs: Assorted.
        These values will map directly to the Leaflet Options. More info
        available here: https://leafletjs.com/reference.html#tooltip

    Examples
    --------
    # Provide fields and aliases, with Style.
    >>> GeoJsonTooltip(
    ...     fields=["CNTY_NM", "census-pop-2015", "census-md-income-2015"],
    ...     aliases=["County", "2015 Census Population", "2015 Median Income"],
    ...     localize=True,
    ...     style=(
    ...         "background-color: grey; color: white; font-family:"
    ...         "courier new; font-size: 24px; padding: 10px;"
    ...     ),
    ... )
    # Provide fields, with labels off and fixed tooltip positions.
    >>> GeoJsonTooltip(fields=("CNTY_NM",), labels=False, sticky=False)
    """

    _template = Template(
        """
    {% macro script(this, kwargs) %}
    {{ this._parent.get_name() }}.bindTooltip("""
        + GeoJsonDetail.base_template
        + """,{{ this.tooltip_options | tojavascript }});
                     {% endmacro %}
                     """
    )

    def __init__(
        self,
        fields: Sequence[str],
        aliases: Optional[Sequence[str]] = None,
        labels: bool = True,
        localize: bool = False,
        style: Optional[str] = None,
        class_name: str = "foliumtooltip",
        sticky: bool = True,
        **kwargs: TypeJsonValue,
    ):
        super().__init__(
            fields=fields,
            aliases=aliases,
            labels=labels,
            localize=localize,
            style=style,
            class_name=class_name,
        )
        self._name = "GeoJsonTooltip"
        kwargs.update({"sticky": sticky, "class_name": class_name})
        self.tooltip_options = kwargs


class GeoJsonPopup(GeoJsonDetail):
    """
    Create a popup feature to bind to each element of a GeoJson layer based on
    its attributes.

    Parameters
    ----------
    fields: list or tuple.
        Labels of GeoJson/TopoJson 'properties' or GeoPandas GeoDataFrame
        columns you'd like to display.
    aliases: list/tuple of strings, same length/order as fields, default None.
        Optional aliases you'd like to display in the tooltip as field name
        instead of the keys of `fields`.
    labels: bool, default True.
        Set to False to disable displaying the field names or aliases.
    localize: bool, default False.
        This will use JavaScript's .toLocaleString() to format 'clean' values
        as strings for the user's location; i.e. 1,000,000.00 comma separators,
        float truncation, etc.
        Available for most of JavaScript's primitive types (any data you'll
        serve into the template).
    style: str, default None.
        HTML inline style properties like font and colors. Will be applied to
        a div with the text in it.

    Examples
    ---
    gjson = folium.GeoJson(gdf).add_to(m)

    folium.features.GeoJsonPopup(fields=['NAME'],
                                labels=False
                                ).add_to(gjson)
    """

    _template = Template(
        """
    {% macro script(this, kwargs) %}
    {{ this._parent.get_name() }}.bindPopup("""
        + GeoJsonDetail.base_template
        + """,{{ this.popup_options | tojavascript }});
                     {% endmacro %}
                     """
    )

    def __init__(
        self,
        fields: Sequence[str],
        aliases: Optional[Sequence[str]] = None,
        labels: bool = True,
        style: str = "margin: auto;",
        class_name: str = "foliumpopup",
        localize: bool = True,
        **kwargs: TypeJsonValue,
    ):
        super().__init__(
            fields=fields,
            aliases=aliases,
            labels=labels,
            localize=localize,
            class_name=class_name,
            style=style,
        )
        self._name = "GeoJsonPopup"
        kwargs.update({"class_name": self.class_name})
        self.popup_options = kwargs


class Choropleth(FeatureGroup):
    """Apply a GeoJSON overlay to the map.

    Plot a GeoJSON overlay on the base map. There is no requirement
    to bind data (passing just a GeoJSON plots a single-color overlay),
    but there is a data binding option to map your columnar data to
    different feature objects with a color scale.

    If data is passed as a Pandas DataFrame, the "columns" and "key-on"
    keywords must be included, the first to indicate which DataFrame
    columns to use, the second to indicate the layer in the GeoJSON
    on which to key the data. The 'columns' keyword does not need to be
    passed for a Pandas series.

    Colors are generated from color brewer (https://colorbrewer2.org/)
    sequential palettes. By default, linear binning is used between
    the min and the max of the values. Custom binning can be achieved
    with the `bins` parameter.

    TopoJSONs can be passed as "geo_data", but the "topojson" keyword must
    also be passed with the reference to the topojson objects to convert.
    See the topojson.feature method in the TopoJSON API reference:
    https://github.com/topojson/topojson/wiki/API-Reference


    Parameters
    ----------
    geo_data: string/object
        URL, file path, or data (json, dict, geopandas, etc) to your GeoJSON
        geometries
    data: Pandas DataFrame or Series, default None
        Data to bind to the GeoJSON.
    columns: tuple with two values, default None
        If the data is a Pandas DataFrame, the columns of data to be bound.
        Must pass column 1 as the key, and column 2 the values.
    key_on: string, default None
        Variable in the `geo_data` GeoJSON file to bind the data to. Must
        start with 'feature' and be in JavaScript objection notation.
        Ex: 'feature.id' or 'feature.properties.statename'.
    bins: int or sequence of scalars or str, default 6
        If `bins` is an int, it defines the number of equal-width
        bins between the min and the max of the values.
        If `bins` is a sequence, it directly defines the bin edges.
        For more information on this parameter, have a look at
        numpy.histogram function.
    fill_color: string, optional
        Area fill color, defaults to blue. Can pass a hex code, color name,
        or if you are binding data, one of the following color brewer palettes:
        'BuGn', 'BuPu', 'GnBu', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'RdPu',
        'YlGn', 'YlGnBu', 'YlOrBr', and 'YlOrRd'.
    nan_fill_color: string, default 'black'
        Area fill color for nan or missing values.
        Can pass a hex code, color name.
    fill_opacity: float, default 0.6
        Area fill opacity, range 0-1.
    nan_fill_opacity: float, default fill_opacity
        Area fill opacity for nan or missing values, range 0-1.
    line_color: string, default 'black'
        GeoJSON geopath line color.
    line_weight: int, default 1
        GeoJSON geopath line weight.
    line_opacity: float, default 1
        GeoJSON geopath line opacity, range 0-1.
    legend_name: string, default empty string
        Title for data legend.
    topojson: string, default None
        If using a TopoJSON, passing "objects.yourfeature" to the topojson
        keyword argument will enable conversion to GeoJSON.
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.
    highlight: boolean, default False
        Enable highlight functionality when hovering over a GeoJSON area.
    use_jenks: bool, default False
        Use jenkspy to calculate bins using "natural breaks"
        (Fisher-Jenks algorithm). This is useful when your data is unevenly
        distributed.
    name : string, optional
        The name of the layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.

    Returns
    -------
    GeoJSON data layer in obj.template_vars

    Examples
    --------
    >>> Choropleth(geo_data="us-states.json", line_color="blue", line_weight=3)
    >>> Choropleth(
    ...     geo_data="geo.json",
    ...     data=df,
    ...     columns=["Data 1", "Data 2"],
    ...     key_on="feature.properties.myvalue",
    ...     fill_color="PuBu",
    ...     bins=[0, 20, 30, 40, 50, 60],
    ... )
    >>> Choropleth(geo_data="countries.json", topojson="objects.countries")
    >>> Choropleth(
    ...     geo_data="geo.json",
    ...     data=df,
    ...     columns=["Data 1", "Data 2"],
    ...     key_on="feature.properties.myvalue",
    ...     fill_color="PuBu",
    ...     bins=[0, 20, 30, 40, 50, 60],
    ...     highlight=True,
    ... )
    """

    def __init__(
        self,
        geo_data: Any,
        data: Optional[Any] = None,
        columns: Optional[Sequence[Any]] = None,
        key_on: Optional[str] = None,
        bins: Union[int, Sequence[float]] = 6,
        fill_color: Optional[str] = None,
        nan_fill_color: str = "black",
        fill_opacity: float = 0.6,
        nan_fill_opacity: Optional[float] = None,
        line_color: str = "black",
        line_weight: float = 1,
        line_opacity: float = 1,
        name: Optional[str] = None,
        legend_name: str = "",
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        topojson: Optional[str] = None,
        smooth_factor: Optional[float] = None,
        highlight: bool = False,
        use_jenks: bool = False,
        **kwargs,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "Choropleth"

        fill_color = fill_color or ("blue" if data is None else "Blues")

        if data is not None and not color_brewer(fill_color):
            raise ValueError(
                "Please pass a valid color brewer code to "
                "fill_local. See docstring for valid codes."
            )

        if nan_fill_opacity is None:
            nan_fill_opacity = fill_opacity

        if "threshold_scale" in kwargs:
            if kwargs["threshold_scale"] is not None:
                bins = kwargs["threshold_scale"]
            warnings.warn(
                "choropleth `threshold_scale` parameter is now depreciated "
                "in favor of the `bins` parameter.",
                DeprecationWarning,
            )

        # Create color_data dict
        if hasattr(data, "set_index"):
            # This is a pd.DataFrame
            assert columns is not None
            color_data = data.set_index(columns[0])[columns[1]].to_dict()  # type: ignore
        elif hasattr(data, "to_dict"):
            # This is a pd.Series
            color_data = data.to_dict()  # type: ignore
        elif data:
            color_data = dict(data)
        else:
            color_data = None

        self.color_scale = None

        if color_data is not None and key_on is not None:
            real_values = np.array(list(color_data.values()))
            real_values = real_values[~np.isnan(real_values)]
            if use_jenks:
                from jenkspy import jenks_breaks

                if not isinstance(bins, int):
                    raise ValueError(
                        f"bins value must be an integer when using Jenks."
                        f' Invalid value "{bins}" received.'
                    )
                bin_edges = np.array(jenks_breaks(real_values, bins), dtype=float)
            else:
                _, bin_edges = np.histogram(real_values, bins=bins)

            bins_min, bins_max = min(bin_edges), max(bin_edges)
            if np.any((real_values < bins_min) | (real_values > bins_max)):
                raise ValueError(
                    "All values are expected to fall into one of the provided "
                    "bins (or to be Nan). Please check the `bins` parameter "
                    "and/or your data."
                )

            # We add the colorscale
            nb_bins = len(bin_edges) - 1
            color_range = color_brewer(fill_color, n=nb_bins)
            self.color_scale = StepColormap(
                color_range,
                index=list(bin_edges),
                vmin=bins_min,
                vmax=bins_max,
                caption=legend_name,
            )

            # then we 'correct' the last edge for numpy digitize
            # (we add a very small amount to fake an inclusive right interval)
            increasing = bin_edges[0] <= bin_edges[-1]
            bin_edges = bin_edges.astype(float)
            bin_edges[-1] = np.nextafter(
                bin_edges[-1], (1 if increasing else -1) * np.inf
            )

            key_on = key_on[8:] if key_on.startswith("feature.") else key_on

            def color_scale_fun(x):
                key_of_x = self._get_by_key(x, key_on)
                if key_of_x is None:
                    raise ValueError(f"key_on `{key_on!r}` not found in GeoJSON.")

                try:
                    value_of_x = color_data[key_of_x]
                except KeyError:
                    try:
                        # try again but match str to int and vice versa
                        if isinstance(key_of_x, int):
                            value_of_x = color_data[str(key_of_x)]
                        elif isinstance(key_of_x, str):
                            value_of_x = color_data[int(key_of_x)]
                        else:
                            return nan_fill_color, nan_fill_opacity
                    except (KeyError, ValueError):
                        return nan_fill_color, nan_fill_opacity

                if np.isnan(value_of_x):
                    return nan_fill_color, nan_fill_opacity

                color_idx = np.digitize(value_of_x, bin_edges, right=False) - 1
                return color_range[color_idx], fill_opacity

        else:

            def color_scale_fun(x):
                return fill_color, fill_opacity

        def style_function(x):
            color, opacity = color_scale_fun(x)
            return {
                "weight": line_weight,
                "opacity": line_opacity,
                "color": line_color,
                "fillOpacity": opacity,
                "fillColor": color,
            }

        def highlight_function(x):
            return {"weight": line_weight + 2, "fillOpacity": fill_opacity + 0.2}

        if topojson:
            self.geojson: Union[TopoJson, GeoJson] = TopoJson(
                geo_data,
                topojson,
                style_function=style_function,
                smooth_factor=smooth_factor,
            )
        else:
            self.geojson = GeoJson(
                geo_data,
                style_function=style_function,
                smooth_factor=smooth_factor,
                highlight_function=highlight_function if highlight else None,
            )

        self.add_child(self.geojson)
        if self.color_scale:
            self.add_child(self.color_scale)

    @classmethod
    def _get_by_key(cls, obj: Union[dict, list], key: str) -> Union[float, str, None]:
        key_parts = key.split(".")
        first_key_part = key_parts[0]
        if first_key_part.isdigit():
            value = obj[int(first_key_part)]
        else:
            value = obj.get(first_key_part, None)  # type: ignore
        if len(key_parts) > 1:
            new_key = ".".join(key_parts[1:])
            return cls._get_by_key(value, new_key)
        else:
            return value

    def render(self, **kwargs):
        """Render the GeoJson/TopoJson and color scale objects."""
        if self.color_scale:
            # ColorMap needs Map as its parent
            assert isinstance(
                self._parent, Map
            ), "Choropleth must be added to a Map object."
            self.color_scale._parent = self._parent

        super().render(**kwargs)


class DivIcon(MacroElement):
    """
    Represents a lightweight icon for markers that uses a simple `div`
    element instead of an image.

    Parameters
    ----------
    icon_size : tuple of 2 int
        Size of the icon image in pixels.
    icon_anchor : tuple of 2 int
        The coordinates of the "tip" of the icon
        (relative to its top left corner).
        The icon will be aligned so that this point is at the
        marker's geographical location.
    popup_anchor : tuple of 2 int
        The coordinates of the point from which popups will "open",
        relative to the icon anchor.
    class_name : string
        A custom class name to assign to the icon.
        Leaflet defaults is 'leaflet-div-icon' which draws a little white
        square with a shadow.  We set it 'empty' in folium.
    html : string
        A custom HTML code to put inside the div element.

    See https://leafletjs.com/reference.html#divicon

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.divIcon({{ this.options|tojavascript }});
        {% endmacro %}
        """
    )  # noqa

    def __init__(
        self,
        html: Optional[str] = None,
        icon_size: Optional[tuple[int, int]] = None,
        icon_anchor: Optional[tuple[int, int]] = None,
        popup_anchor: Optional[tuple[int, int]] = None,
        class_name: str = "empty",
    ):
        super().__init__()
        self._name = "DivIcon"
        self.options = remove_empty(
            html=html,
            icon_size=icon_size,
            icon_anchor=icon_anchor,
            popup_anchor=popup_anchor,
            class_name=class_name,
        )


class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.

    """

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                    "<br>Longitude: " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )  # noqa

    def __init__(self):
        super().__init__()
        self._name = "LatLngPopup"


class ClickForMarker(MacroElement):
    """
    When one clicks on a Map that contains a ClickForMarker,
    a Marker is created at the pointer's position.

    Parameters
    ----------
    popup: str or IFrame or Html, default None
        Text to display in the markers' popups.
        This can also be an Element like IFrame or Html.
        If None, the popups will display the marker's latitude and longitude.
        You can include the latitude and longitude with ${lat} and ${lng}.


    Examples
    --------
    >>> ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")

    """

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                function newMarker(e){
                    var new_mark = L.marker().setLatLng(e.latlng).addTo({{this._parent.get_name()}});
                    new_mark.dragging.enable();
                    new_mark.on('dblclick', function(e){ {{this._parent.get_name()}}.removeLayer(e.target)})
                    var lat = e.latlng.lat.toFixed(4),
                       lng = e.latlng.lng.toFixed(4);
                    new_mark.bindPopup({{ this.popup }});
                    };
                {{this._parent.get_name()}}.on('click', newMarker);
            {% endmacro %}
            """
    )  # noqa

    def __init__(self, popup: Union[IFrame, Html, str, None] = None):
        super().__init__()
        self._name = "ClickForMarker"

        if isinstance(popup, Element):
            popup = popup.render()
        if popup:
            self.popup = "`" + escape_backticks(popup) + "`"  # type: ignore
        else:
            self.popup = '"Latitude: " + lat + "<br>Longitude: " + lng '


class ClickForLatLng(MacroElement):
    """
    When one clicks on a Map that contains a ClickForLatLng,
    the coordinates of the pointer's position are copied to clipboard.

    Parameters
    ==========
    format_str : str, default 'lat + "," + lng'
        The javascript string used to format the text copied to clipboard.
        eg:
        format_str = 'lat + "," + lng'              >> 46.558860,3.397397
        format_str = '"[" + lat + "," + lng + "]"'  >> [46.558860,3.397397]
    alert : bool, default True
        Whether there should be an alert when something has been copied to clipboard.
    """

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                function getLatLng(e){
                    var lat = e.latlng.lat.toFixed(6),
                        lng = e.latlng.lng.toFixed(6);
                    var txt = {{this.format_str}};
                    navigator.clipboard.writeText(txt);
                    {% if this.alert %}alert("Copied to clipboard : \\n    " + txt);{% endif %}
                    };
                {{this._parent.get_name()}}.on('click', getLatLng);
            {% endmacro %}
            """
    )  # noqa

    def __init__(self, format_str: Optional[str] = None, alert: bool = True):
        super().__init__()
        self._name = "ClickForLatLng"
        self.format_str = format_str or 'lat + "," + lng'
        self.alert = alert


class CustomIcon(Icon):
    """
    Create a custom icon, based on an image.

    Parameters
    ----------
    icon_image : string or array-like object
        The data to use as an icon.

        * If string is a path to an image file, its content will be converted and
          embedded.
        * If string is a URL, it will be linked.
        * Otherwise a string will be assumed to be JSON and embedded.
        * If array-like, it will be converted to PNG base64 string and embedded.
    icon_size : tuple of 2 int, optional
        Size of the icon image in pixels.
    icon_anchor : tuple of 2 int, optional
        The coordinates of the "tip" of the icon
        (relative to its top left corner).
        The icon will be aligned so that this point is at the
        marker's geographical location.
    shadow_image :  string, file or array-like object, optional
        The data for the shadow image. If not specified,
        no shadow image will be created.
    shadow_size : tuple of 2 int, optional
        Size of the shadow image in pixels.
    shadow_anchor : tuple of 2 int, optional
        The coordinates of the "tip" of the shadow relative to its
        top left corner (the same as icon_anchor if not specified).
    popup_anchor : tuple of 2 int, optional
        The coordinates of the point from which popups will "open",
        relative to the icon anchor.

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = L.icon({{ this.options|tojavascript }});
        {% endmacro %}
        """
    )  # noqa

    def __init__(
        self,
        icon_image: Any,
        icon_size: Optional[tuple[int, int]] = None,
        icon_anchor: Optional[tuple[int, int]] = None,
        shadow_image: Any = None,
        shadow_size: Optional[tuple[int, int]] = None,
        shadow_anchor: Optional[tuple[int, int]] = None,
        popup_anchor: Optional[tuple[int, int]] = None,
    ):
        super(Icon, self).__init__()
        self._name = "icon"
        self.options = remove_empty(
            icon_url=image_to_url(icon_image),
            icon_size=icon_size,
            icon_anchor=icon_anchor,
            shadow_url=shadow_image and image_to_url(shadow_image),
            shadow_size=shadow_size,
            shadow_anchor=shadow_anchor,
            popup_anchor=popup_anchor,
        )


class ColorLine(FeatureGroup):
    """
    Draw data on a map with specified colors.

    Parameters
    ----------
    positions: iterable of (lat, lon) pairs
        The points on the line. Segments between points will be colored.
    colors: iterable of float
        Values that determine the color of a line segment.
        It must have length equal to `len(positions)-1`.
    colormap: branca.colormap.Colormap or list or tuple
        The colormap to use. If a list or tuple of colors is provided,
        a LinearColormap will be created from it.
    nb_steps: int, default 12
        The colormap will be discretized to this number of colors.
    opacity: float, default 1
        Line opacity, scale 0-1
    weight: int, default 2
        Stroke weight in pixels
    **kwargs
        Further parameters available. See folium.map.FeatureGroup

    Returns
    -------
    A ColorLine object that you can `add_to` a Map.

    """

    def __init__(
        self,
        positions: TypeLine,
        colors: Iterable[float],
        colormap: Union[ColorMap, Sequence[Any], None] = None,
        nb_steps: int = 12,
        weight: Optional[int] = None,
        opacity: Optional[float] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._name = "ColorLine"
        coords = validate_locations(positions)

        if colormap is None:
            cm: StepColormap = LinearColormap(
                ["green", "yellow", "red"],
                vmin=min(colors),
                vmax=max(colors),
            ).to_step(nb_steps)
        elif isinstance(colormap, LinearColormap):
            cm = colormap.to_step(nb_steps)
        elif isinstance(colormap, list) or isinstance(colormap, tuple):
            cm = LinearColormap(
                colormap,
                vmin=min(colors),
                vmax=max(colors),
            ).to_step(nb_steps)
        elif isinstance(colormap, StepColormap):
            cm = colormap
        else:
            raise TypeError(
                f"Unexpected type for argument `colormap`: {type(colormap)}"
            )

        out: dict[str, list[list[list[float]]]] = {}
        for (lat1, lng1), (lat2, lng2), color in zip(coords[:-1], coords[1:], colors):
            out.setdefault(cm(color), []).append([[lat1, lng1], [lat2, lng2]])
        for key, val in out.items():
            self.add_child(PolyLine(val, color=key, weight=weight, opacity=opacity))


class Control(JSCSSMixin, Class):
    """
    Add a Leaflet Control object to the map

    Parameters
    ----------
    control: str
        The javascript class name of the control to be rendered.
    position: str
        One of "bottomright", "bottomleft", "topright", "topleft"

    Examples
    --------

    >>> import folium
    >>> from folium.features import Control, Marker
    >>> from folium.plugins import Geocoder

    >>> m = folium.Map(
    ...     location=[46.603354, 1.8883335], attr=None, zoom_control=False, zoom_start=5
    ... )
    >>> Control("Zoom", position="topleft").add_to(m)
    """

    _template = Template(
        """
      {% macro script(this, kwargs) %}
          var {{ this.get_name() }} = new L.Control.{{this._name}}(
              {% for arg in this.args %}
                  {{ arg | tojavascript }},
              {% endfor %}
              {{ this.options|tojavascript }}
          ).addTo({{ this._parent.get_name() }});
      {% endmacro %}
    """
    )

    def __init__(
        self,
        control: Optional[str] = None,
        *args,
        position: Optional[TypePosition] = None,
        **kwargs,
    ):
        super().__init__()
        if control:
            self._name = control

        if position is not None:
            position = position.lower()  # type: ignore
            if position not in (args := get_args(TypePosition)):
                raise TypeError(f"position must be one of {args}")
            kwargs["position"] = position

        self.args = args
        self.options = remove_empty(**kwargs)
