
from typing import List, Optional, Union

from branca.element import MacroElement
from folium.elements import JSCSSMixin
from folium.template import Template
from folium.utilities import JsCode, remove_empty, validate_location


class WebGLEarth(JSCSSMixin, MacroElement):
    """Create a 3D globe visualization using WebGL Earth.

    Based on: https://www.webglearth.com/

    Parameters
    ----------
    center : list, default [20, 0]
        Initial center of the globe as [lat, lng].
    zoom : float, default 2.5
        Initial zoom level of the globe.
    tile_url : str, optional
        URL template for the tile layer. Defaults to OpenStreetMap tiles.
    tile_subdomains : str, default "abc"
        Subdomains for the tile layer URL.
    height : int, default 600
        Height of the globe container in pixels.
    atmosphere : bool, default True
        Whether to show the atmosphere effect around the globe.

    Examples
    --------
    >>> import folium
    >>> from folium.plugins import WebGLEarth, WebGLEarthMarker

    >>> m = folium.Map()
    >>> globe = WebGLEarth(center=[48.2, 16.4], zoom=4)
    >>> globe.add_to(m)

    >>> marker = WebGLEarthMarker(
    ...     location=[48.2, 16.4],
    ...     popup="Vienna",
    ... )
    >>> marker.add_to(globe)
    """

    _template = Template(
        """
        {% macro header(this, kwargs) %}
            <style>
                #{{ this._parent.get_name() }} {
                    display: none !important;
                }
                #{{ this.container_id }} {
                    height: {{ this.height }}px;
                    width: 100%;
                    position: relative;
                    z-index: 9999;
                }
                .webgl-earth-reset-btn {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    z-index: 10000;
                    background: white;
                    border: 1px solid #ccc;
                    padding: 6px 12px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 13px;
                }
                .webgl-earth-reset-btn:hover {
                    background: #f0f0f0;
                }
            </style>
        {% endmacro %}

        {% macro html(this, kwargs) %}
            <div style="position: relative;">
                <div id="{{ this.container_id }}"></div>
                <button
                    class="webgl-earth-reset-btn"
                    onclick="{{ this.get_name() }}.setView(
                        [{{ this.center[0] }}, {{ this.center[1] }}],
                        {{ this.zoom }}
                    )"
                >
                    &#8679; Reset View
                </button>
            </div>
        {% endmacro %}

        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = WE.map(
                '{{ this.container_id }}',
                {{ this.options | tojavascript }}
            );

            WE.tileLayer(
                {{ this.tile_url | tojson }},
                {
                    attribution: '&copy; OpenStreetMap contributors',
                    subdomains: {{ this.tile_subdomains | tojson }}
                }
            ).addTo({{ this.get_name() }});

            // Block right-click tilt
            (function() {
                var container = document.getElementById('{{ this.container_id }}');
                container.addEventListener('contextmenu', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                });
                container.addEventListener('mousedown', function(e) {
                    if (e.button === 2) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                });
            })();
        {% endmacro %}
    """
    )

    default_js = [
        (
            "webglearth_v2_js",
            "https://www.webglearth.com/v2/api.js",
        ),
    ]

    def __init__(
        self,
        center: Optional[List[float]] = None,
        zoom: float = 2.5,
        tile_url: Optional[str] = None,
        tile_subdomains: str = "abc",
        height: int = 600,
        atmosphere: bool = True,
    ):
        super().__init__()
        self._name = "WebGLEarth"

        if center is None:
            center = [20, 0]
        self.center = validate_location(center)
        if not (-90 <= self.center[0] <= 90) or not (-180 <= self.center[1] <= 180):
            raise ValueError(
                f"Invalid center: {list(self.center)}. "
                "Latitude must be -90..90, longitude -180..180."
            )
        self.zoom = zoom
        self.height = height
        self.tile_url = (
            tile_url or "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        )
        self.tile_subdomains = list(tile_subdomains)
        self.container_id = f"webgl-earth-{self.get_name()}"

        self.options = remove_empty(
            center=list(self.center),
            zoom=zoom,
            atmosphere=atmosphere,
        )


class WebGLEarthMarker(MacroElement):
    """Add a marker to a WebGLEarth globe.

    Parameters
    ----------
    location : list
        Marker location as [lat, lng].
    popup : str, optional
        Text to show in a popup when the marker is clicked.

    Examples
    --------
    >>> globe = WebGLEarth()
    >>> marker = WebGLEarthMarker(
    ...     location=[48.2, 16.4],
    ...     popup="Vienna",
    ... )
    >>> marker.add_to(globe)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = WE.marker(
                [{{ this.location[0] }}, {{ this.location[1] }}]
            ).addTo({{ this._parent.get_name() }});
            {% if this.popup %}
            {{ this.get_name() }}.bindPopup({{ this.popup | tojson }});
            {% endif %}
        {% endmacro %}
    """
    )

    def __init__(
        self,
        location: List[float],
        popup: Optional[str] = None,
    ):
        super().__init__()
        self._name = "WebGLEarthMarker"
        self.location = validate_location(location)
        if not (-90 <= self.location[0] <= 90) or not (-180 <= self.location[1] <= 180):
            raise ValueError(
                f"Invalid location: {list(self.location)}. "
                "Latitude must be -90..90, longitude -180..180."
            )
        self.popup = popup


class WebGLEarthTileLayer(MacroElement):
    """Add an additional tile layer to a WebGLEarth globe.

    Parameters
    ----------
    url : str
        URL template for the tile layer.
    attribution : str, default ""
        Attribution text for the tile layer.
    subdomains : str, default "abc"
        Subdomains for the tile layer URL.
    opacity : float, default 1.0
        Opacity of the tile layer (0.0 to 1.0).

    Examples
    --------
    >>> globe = WebGLEarth()
    >>> tiles = WebGLEarthTileLayer(
    ...     url="https://tiles.example.com/{z}/{x}/{y}.png",
    ...     attribution="Example Tiles",
    ...     opacity=0.7,
    ... )
    >>> tiles.add_to(globe)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = WE.tileLayer(
                {{ this.url | tojson }},
                {{ this.options | tojavascript }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
    """
    )

    def __init__(
        self,
        url: str,
        attribution: str = "",
        subdomains: str = "abc",
        opacity: float = 1.0,
    ):
        super().__init__()
        self._name = "WebGLEarthTileLayer"
        self.url = url
        self.options = remove_empty(
            attribution=attribution,
            subdomains=list(subdomains),
            opacity=opacity,
        )


class WebGLEarthRealtime(JSCSSMixin, MacroElement):
    """Show realtime-updating data on a WebGLEarth globe.

    This is the 3D equivalent of the Realtime plugin.

    Parameters
    ----------
    source_url : str
        URL to fetch JSON data from.
    interval : int, default 5000
        Update interval in milliseconds.
    on_update : str or JsCode
        A JavaScript function called with (data, earth) on each update.
        Use this to parse the response and update markers/layers.

    Examples
    --------
    >>> from folium.utilities import JsCode
    >>> globe = WebGLEarth(center=[0, 0], zoom=1.5)
    >>> iss = WebGLEarthRealtime(
    ...     source_url="https://api.wheretheiss.at/v1/satellites/25544",
    ...     interval=3000,
    ...     on_update=JsCode('''
    ...         function(data, earth) {
    ...             if (window._issMarker) window._issMarker.removeFrom(earth);
    ...             window._issMarker = WE.marker(
    ...                 [data.latitude, data.longitude]
    ...             ).addTo(earth);
    ...         }
    ...     '''),
    ... )
    >>> iss.add_to(globe)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            (function() {
                var earth = {{ this._parent.get_name() }};
                function {{ this.get_name() }}_update() {
                    fetch({{ this.source_url | tojson }})
                        .then(function(response) { return response.json(); })
                        .then(function(data) {
                            var callback = {{ this.on_update.js_code }};
                            callback(data, earth);
                        })
                        .catch(function(err) {
                            console.warn('WebGLEarthRealtime error:', err);
                        });
                }
                {{ this.get_name() }}_update();
                setInterval({{ this.get_name() }}_update, {{ this.interval }});
            })();
        {% endmacro %}
    """
    )

    def __init__(
        self,
        source_url: str,
        interval: int = 5000,
        on_update: Union[JsCode, str, None] = None,
    ):
        super().__init__()
        self._name = "WebGLEarthRealtime"
        self.source_url = source_url
        self.interval = interval
        if on_update is None:
            raise ValueError("on_update is required.")
        self.on_update = JsCode(on_update)
