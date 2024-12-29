"""
Make beautiful, interactive maps with Python and Leaflet.js

"""

import time
import webbrowser
from typing import Any, List, Optional, Sequence, Union

from branca.element import Element, Figure

from folium.elements import JSCSSMixin
from folium.map import Evented, FitBounds, Layer
from folium.raster_layers import TileLayer
from folium.template import Template
from folium.utilities import (
    TypeBounds,
    TypeJsonValue,
    _parse_size,
    parse_font_size,
    remove_empty,
    temp_html_filepath,
    validate_location,
)

_default_js = [
    ("leaflet", "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"),
    ("jquery", "https://code.jquery.com/jquery-3.7.1.min.js"),
    (
        "bootstrap",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js",
    ),
    (
        "awesome_markers",
        "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js",
    ),  # noqa
]

_default_css = [
    ("leaflet_css", "https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"),
    (
        "bootstrap_css",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css",
    ),
    # glyphicons came from Bootstrap 3 and are used for Awesome Markers
    (
        "glyphicons_css",
        "https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css",
    ),
    (
        "awesome_markers_font_css",
        "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css",
    ),  # noqa
    (
        "awesome_markers_css",
        "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css",
    ),  # noqa
    (
        "awesome_rotate_css",
        "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css",
    ),  # noqa
]


class GlobalSwitches(Element):
    _template = Template(
        """
        <script>
            L_NO_TOUCH = {{ this.no_touch |tojson}};
            L_DISABLE_3D = {{ this.disable_3d|tojson }};
        </script>
    """
    )

    def __init__(self, no_touch=False, disable_3d=False):
        super().__init__()
        self._name = "GlobalSwitches"
        self.no_touch = no_touch
        self.disable_3d = disable_3d


class Map(JSCSSMixin, Evented):
    """Create a Map with Folium and Leaflet.js

    Generate a base map of given width and height with either default
    tilesets or a custom tileset URL. Folium has built-in all tilesets
    available in the ``xyzservices`` package. For example, you can pass
    any of the following to the "tiles" keyword:

        - "OpenStreetMap"
        - "CartoDB Positron"
        - "CartoDB Voyager"

    Explore more provider names available in ``xyzservices`` here:
    https://leaflet-extras.github.io/leaflet-providers/preview/.

    You can also pass a custom tileset by passing a
    :class:`xyzservices.TileProvider` or a Leaflet-style
    URL to the tiles parameter: ``https://{s}.yourtiles.com/{z}/{x}/{y}.png``.

    Parameters
    ----------
    location: tuple or list, default None
        Latitude and Longitude of Map (Northing, Easting).
    width: pixel int or percentage string (default: '100%')
        Width of the map.
    height: pixel int or percentage string (default: '100%')
        Height of the map.
    tiles: str or TileLayer or :class:`xyzservices.TileProvider`, default 'OpenStreetMap'
        Map tileset to use. Can choose from a list of built-in tiles,
        pass a :class:`xyzservices.TileProvider`,
        pass a custom URL, pass a TileLayer object,
        or pass `None` to create a map without tiles.
        For more advanced tile layer options, use the `TileLayer` class.
    min_zoom: int, optional, default 0
        Minimum allowed zoom level for the tile layer that is created.
        Filled by xyzservices by default.
    max_zoom: int, optional, default 18
        Maximum allowed zoom level for the tile layer that is created.
        Filled by xyzservices by default.
    zoom_start: int, default 10
        Initial zoom level for the map.
    attr: string, default None
        Map tile attribution; only required if passing custom tile URL.
    crs : str, default 'EPSG3857'
        Defines coordinate reference systems for projecting geographical points
        into pixel (screen) coordinates and back.
        You can use Leaflet's values :
        * EPSG3857 : The most common CRS for online maps, used by almost all
        free and commercial tile providers. Uses Spherical Mercator projection.
        Set in by default in Map's crs option.
        * EPSG4326 : A common CRS among GIS enthusiasts.
        Uses simple Equirectangular projection.
        * EPSG3395 : Rarely used by some commercial tile providers.
        Uses Elliptical Mercator projection.
        * Simple : A simple CRS that maps longitude and latitude into
        x and y directly. May be used for maps of flat surfaces
        (e.g. game maps). Note that the y axis should still be inverted
        (going from bottom to top).
    control_scale : bool, default False
        Whether to add a control scale on the map.
    prefer_canvas : bool, default False
        Forces Leaflet to use the Canvas back-end (if available) for
        vector layers instead of SVG. This can increase performance
        considerably in some cases (e.g. many thousands of circle
        markers on the map).
    no_touch : bool, default False
        Forces Leaflet to not use touch events even if it detects them.
    disable_3d : bool, default False
        Forces Leaflet to not use hardware-accelerated CSS 3D
        transforms for positioning (which may cause glitches in some
        rare environments) even if they're supported.
    zoom_control : bool or position string, default True
        Display zoom controls on the map. The default `True` places it in the top left corner.
        Other options are 'topleft', 'topright', 'bottomleft' or 'bottomright'.
    font_size : int or float or string (default: '1rem')
        The font size to use for Leaflet, can either be a number or a
        string ending in 'rem', 'em', or 'px'.
    **kwargs
        Additional keyword arguments are passed to Leaflets Map class:
        https://leafletjs.com/reference.html#map

    Returns
    -------
    Folium Map Object

    Examples
    --------
    >>> m = folium.Map(location=[45.523, -122.675], width=750, height=500)
    >>> m = folium.Map(location=[45.523, -122.675], tiles="cartodb positron")
    >>> m = folium.Map(
    ...     location=[45.523, -122.675],
    ...     zoom_start=2,
    ...     tiles="https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=mytoken",
    ...     attr="Mapbox attribution",
    ... )

    """  # noqa

    _template = Template(
        """
        {% macro header(this, kwargs) %}
            <meta name="viewport" content="width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <style>
                #{{ this.get_name() }} {
                    position: {{this.position}};
                    width: {{this.width[0]}}{{this.width[1]}};
                    height: {{this.height[0]}}{{this.height[1]}};
                    left: {{this.left[0]}}{{this.left[1]}};
                    top: {{this.top[0]}}{{this.top[1]}};
                }
                .leaflet-container { font-size: {{this.font_size}}; }
            </style>
        {% endmacro %}

        {% macro html(this, kwargs) %}
            <div class="folium-map" id={{ this.get_name()|tojson }} ></div>
        {% endmacro %}

        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.map(
                {{ this.get_name()|tojson }},
                {
                    center: {{ this.location|tojson }},
                    crs: L.CRS.{{ this.crs }},
                    ...{{this.options|tojavascript}}

                }
            );

            {%- if this.control_scale %}
            L.control.scale().addTo({{ this.get_name() }});
            {%- endif %}

            {%- if this.zoom_control_position %}
            L.control.zoom( { position: {{ this.zoom_control|tojson }} } ).addTo({{ this.get_name() }});
            {%- endif %}

            {% if this.objects_to_stay_in_front %}
            function objects_in_front() {
                {%- for obj in this.objects_to_stay_in_front %}
                    {{ obj.get_name() }}.bringToFront();
                {%- endfor %}
            };
            {{ this.get_name() }}.on("overlayadd", objects_in_front);
            $(document).ready(objects_in_front);
            {%- endif %}

        {% endmacro %}
        """
    )

    # use the module variables for backwards compatibility
    default_js = _default_js
    default_css = _default_css

    def __init__(
        self,
        location: Optional[Sequence[float]] = None,
        width: Union[str, float] = "100%",
        height: Union[str, float] = "100%",
        left: Union[str, float] = "0%",
        top: Union[str, float] = "0%",
        position: str = "relative",
        tiles: Union[str, TileLayer, None] = "OpenStreetMap",
        attr: Optional[str] = None,
        min_zoom: Optional[int] = None,
        max_zoom: Optional[int] = None,
        zoom_start: int = 10,
        min_lat: float = -90,
        max_lat: float = 90,
        min_lon: float = -180,
        max_lon: float = 180,
        max_bounds: bool = False,
        crs: str = "EPSG3857",
        control_scale: bool = False,
        prefer_canvas: bool = False,
        no_touch: bool = False,
        disable_3d: bool = False,
        png_enabled: bool = False,
        zoom_control: Union[bool, str] = True,
        font_size: str = "1rem",
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "Map"

        self._png_image: Optional[bytes] = None
        self.png_enabled = png_enabled

        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0.0, 0.0]
            zoom_start = 1
        else:
            self.location = validate_location(location)

        Figure().add_child(self)

        # Map Size Parameters.
        self.width = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position
        self.font_size = parse_font_size(font_size)

        max_bounds_array = (
            [[min_lat, min_lon], [max_lat, max_lon]] if max_bounds else None
        )

        self.crs = crs
        self.control_scale = control_scale

        # Zoom control position specified ?
        if isinstance(zoom_control, str):
            self.zoom_control_position = True
            if zoom_control not in {"topleft", "topright", "bottomleft", "bottomright"}:
                raise ValueError(
                    "Incorrect value for `zoom_control`, choose from 'topleft', 'topright', 'bottomleft' or 'bottomright'."
                )
            self.zoom_control = zoom_control
        else:
            self.zoom_control_position = False

        self.options = remove_empty(
            max_bounds=max_bounds_array,
            zoom=zoom_start,
            zoom_control=False if self.zoom_control_position else zoom_control,
            prefer_canvas=prefer_canvas,
            **kwargs,
        )

        self.global_switches = GlobalSwitches(no_touch, disable_3d)

        self.objects_to_stay_in_front: List[Layer] = []

        if isinstance(tiles, TileLayer):
            self.add_child(tiles)
        elif tiles:
            tile_layer = TileLayer(
                tiles=tiles, attr=attr, min_zoom=min_zoom, max_zoom=max_zoom
            )
            self.add_child(tile_layer, name=tile_layer.tile_name)

    def _repr_html_(self, **kwargs) -> str:
        """Displays the HTML Map in a Jupyter notebook."""
        if self._parent is None:
            self.add_to(Figure())
            self._parent: Figure
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out

    def _to_png(self, delay: int = 3, driver: Any = None) -> bytes:
        """Export the HTML to byte representation of a PNG image.

        Uses selenium to render the HTML and record a PNG. You may need to
        adjust the `delay` time keyword argument if maps render without data or tiles.

        Uses a headless Firefox webdriver by default, though you can provide your own.

        Examples
        --------
        >>> m._to_png()
        >>> m._to_png(time=10)  # Wait 10 seconds between render and snapshot.

        """
        if self._png_image is None:
            if driver is None:
                from selenium import webdriver

                options = webdriver.firefox.options.Options()
                options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)

            html = self.get_root().render()
            with temp_html_filepath(html) as fname:
                # We need the tempfile to avoid JS security issues.
                driver.get(f"file:///{fname}")
                driver.fullscreen_window()
                time.sleep(delay)
                div = driver.find_element("class name", "folium-map")
                png = div.screenshot_as_png
                driver.quit()
            self._png_image = png
        return self._png_image

    def _repr_png_(self) -> Optional[bytes]:
        """Displays the PNG Map in a Jupyter notebook."""
        # The notebook calls all _repr_*_ by default.
        # We don't want that here b/c this one is quite slow.
        if not self.png_enabled:
            return None
        return self._to_png()

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        # Set global switches
        figure.header.add_child(self.global_switches, name="global_switches")

        figure.header.add_child(
            Element(
                "<style>html, body {"
                "width: 100%;"
                "height: 100%;"
                "margin: 0;"
                "padding: 0;"
                "}"
                "</style>"
            ),
            name="css_style",
        )

        figure.header.add_child(
            Element(
                "<style>#map {"
                "position:absolute;"
                "top:0;"
                "bottom:0;"
                "right:0;"
                "left:0;"
                "}"
                "</style>"
            ),
            name="map_style",
        )

        super().render(**kwargs)

    def show_in_browser(self) -> None:
        """Display the Map in the default web browser."""
        with temp_html_filepath(self.get_root().render()) as fname:
            webbrowser.open("file://" + fname)
            print(
                "Your map should have been opened in your browser automatically."
                "\nPress ctrl+c to return."
            )
            # Block until stopped by user, afterwards remove the temporary file
            try:
                while True:
                    time.sleep(100)
            except KeyboardInterrupt:
                pass

    def fit_bounds(
        self,
        bounds: TypeBounds,
        padding_top_left: Optional[Sequence[float]] = None,
        padding_bottom_right: Optional[Sequence[float]] = None,
        padding: Optional[Sequence[float]] = None,
        max_zoom: Optional[int] = None,
    ) -> None:
        """Fit the map to contain a bounding box with the
        maximum zoom level possible.

        Parameters
        ----------
        bounds: list of (latitude, longitude) points
            Bounding box specified as two points [southwest, northeast]
        padding_top_left: (x, y) point, default None
            Padding in the top left corner. Useful if some elements in
            the corner, such as controls, might obscure objects you're zooming
            to.
        padding_bottom_right: (x, y) point, default None
            Padding in the bottom right corner.
        padding: (x, y) point, default None
            Equivalent to setting both top left and bottom right padding to
            the same value.
        max_zoom: int, default None
            Maximum zoom to be used.

        Examples
        --------
        >>> m.fit_bounds([[52.193636, -2.221575], [52.636878, -1.139759]])

        """
        self.add_child(
            FitBounds(
                bounds,
                padding_top_left=padding_top_left,
                padding_bottom_right=padding_bottom_right,
                padding=padding,
                max_zoom=max_zoom,
            )
        )

    def keep_in_front(self, *args: Layer) -> None:
        """Pass one or multiple layers that must stay in front.

        The ordering matters, the last one is put on top.

        Parameters
        ----------
        *args :
            Variable length argument list. Any folium object that counts as an
            overlay. For example FeatureGroup or TileLayer.
            Does not work with markers, for those use z_index_offset.
        """
        for obj in args:
            self.objects_to_stay_in_front.append(obj)
