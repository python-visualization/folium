from typing import Union

from branca.element import MacroElement

from folium.elements import JSCSSMixin
from folium.template import Template
from folium.utilities import JsCode, TypeJsFunctionArg


class Realtime(JSCSSMixin, MacroElement):
    """Put realtime data on a Leaflet map: live tracking GPS units,
    sensor data or just about anything.

    Based on: https://github.com/perliedman/leaflet-realtime

    Parameters
    ----------
    source: str, dict, JsCode
        The source can be one of:

        * a string with the URL to get data from
        * a dict that is passed to javascript's `fetch` function
          for fetching the data
        * a `folium.JsCode` object in case you need more freedom.
    start: bool, default True
        Should automatic updates be enabled when layer is added
        on the map and stopped when layer is removed from the map
    interval: int, default 60000
        Automatic update interval, in milliseconds
    get_feature_id: str or JsCode, optional
        A JS function with a geojson `feature` as parameter
        default returns `feature.properties.id`
        Function to get an identifier to uniquely identify a feature over time
    update_feature: str or JsCode, optional
        A JS function with a geojson `feature` as parameter
        Used to update an existing feature's layer;
        by default, points (markers) are updated, other layers are discarded
        and replaced with a new, updated layer.
        Allows to create more complex transitions,
        for example, when a feature is updated
    remove_missing: bool, default False
        Should missing features between updates been automatically
        removed from the layer


    Other keyword arguments are passed to the GeoJson layer, so you can pass
    `style`, `point_to_layer` and/or `on_each_feature`. Make sure to wrap
    Javascript functions in the JsCode class.

    Examples
    --------
    >>> from folium import JsCode
    >>> m = folium.Map(location=[40.73, -73.94], zoom_start=12)
    >>> rt = Realtime(
    ...     "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/subway_stations.geojson",
    ...     get_feature_id="(f) => { return f.properties.objectid; }",
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
            var {{ this.get_name() }} = new L.realtime(
                {{ this.src|tojavascript }},
                {{ this.options|tojavascript }}
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
        source: Union[str, dict, JsCode],
        start: bool = True,
        interval: int = 60000,
        get_feature_id: TypeJsFunctionArg = None,
        update_feature: TypeJsFunctionArg = None,
        remove_missing: bool = False,
        **kwargs
    ):
        super().__init__()
        self._name = "Realtime"
        self.src = source
        self.options = dict(
            start=start,
            interval=interval,
            get_feature_id=JsCode.optional_create(get_feature_id),
            update_feature=JsCode.optional_create(update_feature),
            remove_missing=remove_missing,
            **kwargs
        )
