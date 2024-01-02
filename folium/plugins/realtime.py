from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.utilities import JsCode, camelize, parse_options


class Realtime(JSCSSMixin, MacroElement):
    """Put realtime data on a Leaflet map: live tracking GPS units,
    sensor data or just about anything.

    Based on: https://github.com/perliedman/leaflet-realtime

    Parameters
    ----------
    source :
        The source can be one of:
        * a string with the URL to get data from
        * a dict that is passed to javascript's `fetch` function
          for fetching the data
        * a folium.utilities.JsCode object in case you need more freedom.
    start : bool, default True
        Should automatic updates be enabled when layer is added
        on the map and stopped when layer is removed from the map
    interval : int, default 60000
        Automatic update interval, in milliseconds
    get_feature_id : folium.utilities.JsCode
        A function with a geojson `feature` as parameter
        default returns `feature.properties.id`
        Function to get an identifier uniquely identify a feature over time
    update_feature : folium.utilities.JsCode
        A function with a geojson `feature` as parameter
        Used to update an existing feature's layer;
        by default, points (markers) are updated, other layers are discarded
        and replaced with a new, updated layer.
        Allows to create more complex transitions,
        for example, when a feature is updated
    remove_missing : bool, default False
        Should missing features between updates been automatically
        removed from the layer

    Other parameters are passed to the GeoJson layer, so you can pass
        `style`, `point_to_layer` and/or `on_each_feature`.

    Examples
    --------
    >>> from folium.utilities import JsCode
    >>> m = folium.Map(location=[40.73, -73.94], zoom_start=12)
    >>> rt = Realtime(
    ...     "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson",
    ...     get_feature_id=JsCode("(f) => { return f.properties.objectid; }"),
    ...     point_to_layer=JsCode(
    ...         "(f, latlng) => { return L.circleMarker(latlng, {radius: 8, fillOpacity: 0.2})}"
    ...     ),
    ...     interval=10000,
    ... )
    >>> rt.add_to(m)
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var options = {{this.options|tojson}};
            {% for key, value in this.functions.items() %}
            options["{{key}}"] = {{ value }};
            {% endfor %}

            var {{ this.get_name() }} = new L.realtime(
            {% if this.src is string or this.src is mapping -%}
                {{ this.src|tojson }},
            {% else -%}
                {{ this.src.js_code }},
            {% endif -%}
                options
            );
            {{ this._parent.get_name() }}.addLayer(
                {{ this.get_name() }}._container);
        {% endmacro %}
    """
    )

    default_js = [
        (
            "Leaflet_Realtime_js",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-realtime/2.2.0/leaflet-realtime.js",
        )
    ]

    def __init__(
        self,
        source,
        start=None,
        interval=None,
        get_feature_id=None,
        update_feature=None,
        remove_missing=None,
        **kwargs
    ):
        super().__init__()
        self._name = "Realtime"
        self.src = source

        if start is not None:
            kwargs["start"] = start
        if interval is not None:
            kwargs["interval"] = interval
        if get_feature_id is not None:
            kwargs["get_feature_id"] = get_feature_id
        if update_feature is not None:
            kwargs["update_feature"] = update_feature
        if remove_missing is not None:
            kwargs["remove_missing"] = remove_missing

        # extract JsCode objects
        self.functions = {}
        for key, value in list(kwargs.items()):
            if isinstance(value, JsCode):
                self.functions[camelize(key)] = value.js_code
                kwargs.pop(key)

        self.options = parse_options(**kwargs)
