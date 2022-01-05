"""
Wraps leaflet TileLayer, WmsTileLayer (TileLayer.WMS), ImageOverlay, and VideoOverlay

"""

from branca.element import Element, Figure

from folium.map import Layer
from folium.utilities import image_to_url, mercator_transform, parse_options

from jinja2 import Environment, PackageLoader, Template


ENV = Environment(loader=PackageLoader('folium', 'templates'))


class TileLayer(Layer):
    """
    Create a tile layer to append on a Map.

    Parameters
    ----------
    tiles: str, default 'OpenStreetMap'
        Map tileset to use. Can choose from this list of built-in tiles:
            - "OpenStreetMap"
            - "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"
            - "CartoDB positron", "CartoDB dark_matter"

        You can pass a custom tileset to Folium by passing a Leaflet-style
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
        Whether the layer will be shown on opening (only for overlays).
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
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer(
                {{ this.tiles|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    def __init__(self, tiles='OpenStreetMap', min_zoom=0, max_zoom=18,
                 max_native_zoom=None, attr=None,
                 detect_retina=False, name=None, overlay=False,
                 control=True, show=True, no_wrap=False, subdomains='abc',
                 tms=False, opacity=1, **kwargs):

        self.tile_name = (name if name is not None else
                          ''.join(tiles.lower().strip().split()))
        super(TileLayer, self).__init__(name=self.tile_name, overlay=overlay,
                                        control=control, show=show)
        self._name = 'TileLayer'
        self._env = ENV

        tiles_flat = ''.join(tiles.lower().strip().split())
        if tiles_flat in {'cloudmade', 'mapbox', 'mapboxbright', 'mapboxcontrolroom'}:
            # added in May 2020 after v0.11.0, remove in a future release
            raise ValueError(
                'Built-in templates for Mapbox and Cloudmade have been removed. '
                'You can still use these providers by passing a URL to the `tiles` '
                'argument. See the documentation of the `TileLayer` class.'
            )
        templates = list(self._env.list_templates(
            filter_func=lambda x: x.startswith('tiles/')))
        tile_template = 'tiles/' + tiles_flat + '/tiles.txt'
        attr_template = 'tiles/' + tiles_flat + '/attr.txt'

        if tile_template in templates and attr_template in templates:
            self.tiles = self._env.get_template(tile_template).render()
            attr = self._env.get_template(attr_template).render()
        else:
            self.tiles = tiles
            if not attr:
                raise ValueError('Custom tiles must have an attribution.')

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
            **kwargs
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
        Whether the layer will be shown on opening (only for overlays).
    **kwargs : additional keyword arguments
        Passed through to the underlying tileLayer.wms object and can be used
        for setting extra tileLayer.wms parameters or as extra parameters in
        the WMS request.

    See https://leafletjs.com/reference-1.6.0.html#tilelayer-wms
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.tileLayer.wms(
                {{ this.url|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)  # noqa

    def __init__(self, url, layers, styles='', fmt='image/jpeg',
                 transparent=False, version='1.1.1', attr='',
                 name=None, overlay=True, control=True, show=True, **kwargs):
        super(WmsTileLayer, self).__init__(name=name, overlay=overlay,
                                           control=control, show=show)
        self.url = url
        kwargs['format'] = fmt
        self.options = parse_options(
            layers=layers,
            styles=styles,
            transparent=transparent,
            version=version,
            attribution=attr,
            **kwargs
        )


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
    pixelated: bool, default True
        Sharp sharp/crips (True) or aliased corners (False).
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).

    See https://leafletjs.com/reference-1.6.0.html#imageoverlay for more
    options.

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.imageOverlay(
                {{ this.url|tojson }},
                {{ this.bounds|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    def __init__(self, image, bounds, origin='upper', colormap=None,
                 mercator_project=False, pixelated=True,
                 name=None, overlay=True, control=True, show=True, **kwargs):
        super(ImageOverlay, self).__init__(name=name, overlay=overlay,
                                           control=control, show=show)
        self._name = 'ImageOverlay'
        self.bounds = bounds
        self.options = parse_options(**kwargs)
        self.pixelated = pixelated
        if mercator_project:
            image = mercator_transform(
                image,
                [bounds[0][0], bounds[1][0]],
                origin=origin
            )

        self.url = image_to_url(image, origin=origin, colormap=colormap)

    def render(self, **kwargs):
        super(ImageOverlay, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
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
            figure.header.add_child(Element(pixelated), name='leaflet-image-layer')  # noqa

    def _get_self_bounds(self):
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
        Whether the layer will be shown on opening (only for overlays).
    **kwargs:
        Other valid (possibly inherited) options. See:
        https://leafletjs.com/reference-1.6.0.html#videooverlay

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.videoOverlay(
                {{ this.video_url|tojson }},
                {{ this.bounds|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    def __init__(self, video_url, bounds, autoplay=True, loop=True,
                 name=None, overlay=True, control=True, show=True, **kwargs):
        super(VideoOverlay, self).__init__(name=name, overlay=overlay,
                                           control=control, show=show)
        self._name = 'VideoOverlay'
        self.video_url = video_url

        self.bounds = bounds
        self.options = parse_options(
            autoplay=autoplay,
            loop=loop,
            **kwargs
        )

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        return self.bounds
