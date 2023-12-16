from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.utilities import parse_options, JsCode


class Realtime(JSCSSMixin, MacroElement):
    """Put realtime data on a Leaflet map: live tracking GPS units,
    sensor data or just about anything.

    Based on: https://github.com/perliedman/leaflet-realtime

    Parameters
    ----------
    start : bool, default True
        Should automatic updates be enabled when layer is added
        on the map and stopped when layer is removed from the map
    interval : int, default 60000
        Automatic update interval, in milliseconds
    getFeatureId : function, default returns `feature.properties.id`
        Function to get an identifier uniquely identify a feature over time
    updateFeature : function
        Used to update an existing feature's layer;
        by default, points (markers) are updated, other layers are discarded
        and replaced with a new, updated layer.
        Allows to create more complex transitions,
        for example, when a feature is updated
    removeMissing : bool, default False
        Should missing features between updates been automatically
        removed from the layer

    Other parameters are passed to the GeoJson layer, so you can pass
        `style`, `pointToLayer` and/or `onEachFeature`.

    Examples
    --------
    >>> from folium.utilities import JsCode
    >>> m = folium.Map()
    >>> rt = Realtime("https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_geography_regions_elevation_points.geojson",
    ...                getFeatureId=JsCode("function(f) { return f.properties.name; }"),
    ...                interval=10000)
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
                {{ this.src|tojson }},
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
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-realtime/2.2.0/leaflet-realtime.js",  # NoQA
        )
    ]

    def __init__(self, src, **kwargs):
        super().__init__()
        self._name = "Realtime"
        self.src = src

        # extract JsCode objects
        self.functions = {}
        for key, value in kwargs.items():
            if isinstance(value, JsCode):
                self.functions[key] = value.js_code

        # and remove them from kwargs
        for key in self.functions:
            kwargs.pop(key)

        # the container is special, as we
        # do not allow it to be set (yet)
        # from python
        self.options = parse_options(container=None, **kwargs)
