"""
Wraps leaflet TileLayer, WmsTileLayer (TileLayer.WMS), ImageOverlay, and VideoOverlay

"""
from typing import Any, Callable, Optional, Union

import xyzservices
from branca.element import Element, Figure
from jinja2 import Template

from folium.map import Layer
from folium.utilities import (
    TypeBounds,
    TypeJsonValue,
    image_to_url,
    mercator_transform,
    parse_options,
)


class TileLayer(Layer):
    """
    Create a tile layer to append on a Map.

    Parameters
    ----------
    tiles: str or :class:`xyzservices.TileProvider`, default 'OpenStreetMap'
        Map tileset to use. Folium has built-in all tilesets
        available in the ``xyzservices`` package. For example, you can pass
        any of the following to the "tiles" keyword:

            - "OpenStreetMap"
            - "CartoDB Positron"
            - "CartoBD Voyager"
            - "NASAGIBS Blue Marble"

        You can pass a custom tileset to Folium by passing a
        :class:`xyzservices.TileProvider` or a Leaflet-style
        URL to the tiles parameter: ``http://{s}.yourtiles.com/{z}/{x}/{y}.png``.

        You can find a list of free tile providers here:
        ``http://leaflet-extras.github.io/leaflet-providers/preview/``.
        Be sure to check their terms and conditions and to provide attribution
        with the `attr` keyword.
    min_zoom: int, default 0
        Minimum allowed zoom level for this tile layer.
    max_zoom: int, default 18
        Maximum allowed zoom level for this tile layer.
    max_native_zoom: int, default None
        The highest zoom level at which the tile server can provide tiles.
        If provided you can zoom in past this level. Else tiles will turn grey.
    attr: string, default None
        Map tile attribution; only required if passing custom tile URL.
    detect_retina: bool, default False
        If true and user is on a retina display, it will request four
        tiles of half the specified size and a bigger zoom level in place
        of one to utilize the high resolution.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
        When adding multiple base layers, use this parameter to select which one
        should be shown when opening the map, by not showing the others.
    subdomains: list of strings, default ['abc']
        Subdomains of the tile service.
    tms: bool, default False
        If true, inverses Y axis numbering for tiles (turn this on for TMS
        services).
    opacity: float, default 1
        Sets the opacity for the layer.
    **kwargs : additional keyword arguments
        Other keyword arguments are passed as options to the Leaflet tileLayer
        object.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer(
                {{ this.tiles|tojson }},
                {{ this.options|tojson }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        tiles: Union[str, xyzservices.TileProvider] = "OpenStreetMap",
        min_zoom: int = 0,
        max_zoom: int = 18,
        max_native_zoom: Optional[int] = None,
        attr: Optional[str] = None,
        detect_retina: bool = False,
        name: Optional[str] = None,
        overlay: bool = False,
        control: bool = True,
        show: bool = True,
        no_wrap: bool = False,
        subdomains: str = "abc",
        tms: bool = False,
        opacity: float = 1,
        **kwargs,
    ):
        if isinstance(tiles, str):
            if tiles.lower() == "openstreetmap":
                tiles = "OpenStreetMap Mapnik"
                if name is None:
                    name = "openstreetmap"
            try:
                tiles = xyzservices.providers.query_name(tiles)
            except ValueError:
                # no match, likely a custom URL
                pass

        if isinstance(tiles, xyzservices.TileProvider):
            attr = attr if attr else tiles.html_attribution  # type: ignore
            min_zoom = tiles.get("min_zoom", min_zoom)
            max_zoom = tiles.get("max_zoom", max_zoom)
            subdomains = tiles.get("subdomains", subdomains)
            if name is None:
                name = tiles.name.replace(".", "").lower()
            tiles = tiles.build_url(fill_subdomain=False, scale_factor="{r}")  # type: ignore

        self.tile_name = (
            name if name is not None else "".join(tiles.lower().strip().split())
        )
        super().__init__(
            name=self.tile_name, overlay=overlay, control=control, show=show
        )
        self._name = "TileLayer"

        self.tiles = tiles
        if not attr:
            raise ValueError("Custom tiles must have an attribution.")

        self.options = parse_options(
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            max_native_zoom=max_native_zoom or max_zoom,
            no_wrap=no_wrap,
            attribution=attr,
            subdomains=subdomains,
            detect_retina=detect_retina,
            tms=tms,
            opacity=opacity,
            **kwargs,
        )


class WmsTileLayer(Layer):
    """
    Creates a Web Map Service (WMS) layer.

    Parameters
    ----------
    url : str
        The url of the WMS server.
    layers : str
        Comma-separated list of WMS layers to show.
    styles : str, optional
        Comma-separated list of WMS styles.
    fmt : str, default 'image/jpeg'
        The format of the service output. Ex: 'image/png'
    transparent: bool, default False
        Whether the layer shall allow transparency.
    version : str, default '1.1.1'
        Version of the WMS service to use.
    attr : str, default ''
        The attribution of the service.
        Will be displayed in the bottom right corner.
    name : string, optional
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    **kwargs : additional keyword arguments
        Passed through to the underlying tileLayer.wms object and can be used
        for setting extra tileLayer.wms parameters or as extra parameters in
        the WMS request.

    See https://leafletjs.com/reference.html#tilelayer-wms
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer.wms(
                {{ this.url|tojson }},
                {{ this.options|tojson }}
            );
        {% endmacro %}
        """
    )  # noqa

    def __init__(
        self,
        url: str,
        layers: str,
        styles: str = "",
        fmt: str = "image/jpeg",
        transparent: bool = False,
        version: str = "1.1.1",
        attr: str = "",
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        **kwargs,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self.url = url
        kwargs["format"] = fmt
        cql_filter = kwargs.pop("cql_filter", None)
        self.options = parse_options(
            layers=layers,
            styles=styles,
            transparent=transparent,
            version=version,
            attribution=attr,
            **kwargs,
        )
        if cql_filter:
            # special parameter that shouldn't be camelized
            self.options["cql_filter"] = cql_filter


class ImageOverlay(Layer):
    """
    Used to load and display a single image over specific bounds of
    the map, implements ILayer interface.

    Parameters
    ----------
    image: string, file or array-like object
        The data you want to draw on the map.
        * If string, it will be written directly in the output file.
        * If file, it's content will be converted as embedded in the output file.
        * If array-like, it will be converted to PNG base64 string and embedded in the output.
    bounds: list
        Image bounds on the map in the form
         [[lat_min, lon_min], [lat_max, lon_max]]
    opacity: float, default Leaflet's default (1.0)
    alt: string, default Leaflet's default ('')
    origin: ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or
        lower left corner of the axes.
    colormap: callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4,
        with values between 0 and 1.
        Hint: you can use colormaps from `matplotlib.cm`.
    mercator_project: bool, default False.
        Used only for array-like image.  Transforms the data to
        project (longitude, latitude) coordinates to the Mercator projection.
        Beware that this will only work if `image` is an array-like object.
        Note that if used the image will be clipped beyond latitude -85 and 85.
    pixelated: bool, default True
        Sharp sharp/crips (True) or aliased corners (False).
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.

    See https://leafletjs.com/reference.html#imageoverlay for more
    options.

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.imageOverlay(
                {{ this.url|tojson }},
                {{ this.bounds|tojson }},
                {{ this.options|tojson }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        image: Any,
        bounds: TypeBounds,
        origin: str = "upper",
        colormap: Optional[Callable] = None,
        mercator_project: bool = False,
        pixelated: bool = True,
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        **kwargs,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "ImageOverlay"
        self.bounds = bounds
        self.options = parse_options(**kwargs)
        self.pixelated = pixelated
        if mercator_project:
            image = mercator_transform(
                image, (bounds[0][0], bounds[1][0]), origin=origin
            )

        self.url = image_to_url(image, origin=origin, colormap=colormap)

    def render(self, **kwargs) -> None:
        super().render()

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."
        if self.pixelated:
            pixelated = """
                <style>
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                </style>
            """
            figure.header.add_child(
                Element(pixelated), name="leaflet-image-layer"
            )  # noqa

    def _get_self_bounds(self) -> TypeBounds:
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return self.bounds


class VideoOverlay(Layer):
    """
    Used to load and display a video over the map.

    Parameters
    ----------
    video_url: str
        URL of the video
    bounds: list
        Video bounds on the map in the form
         [[lat_min, lon_min], [lat_max, lon_max]]
    autoplay: bool, default True
    loop: bool, default True
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    **kwargs:
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference.html#videooverlay

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.videoOverlay(
                {{ this.video_url|tojson }},
                {{ this.bounds|tojson }},
                {{ this.options|tojson }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        video_url: str,
        bounds: TypeBounds,
        autoplay: bool = True,
        loop: bool = True,
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        **kwargs: TypeJsonValue,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "VideoOverlay"
        self.video_url = video_url

        self.bounds = bounds
        self.options = parse_options(autoplay=autoplay, loop=loop, **kwargs)

    def _get_self_bounds(self) -> TypeBounds:
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        return self.bounds
