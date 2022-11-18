from jinja2 import Template

from folium.plugins.marker_cluster import MarkerCluster
from folium.utilities import if_pandas_df_convert_to_numpy, validate_location


class FastMarkerCluster(MarkerCluster):
    """
    Add marker clusters to a map using in-browser rendering.
    Using FastMarkerCluster it is possible to render 000's of
    points far quicker than the MarkerCluster class.

    Be aware that the FastMarkerCluster class passes an empty
    list to the parent class' __init__ method during initialisation.
    This means that the add_child method is never called, and
    no reference to any marker data are retained. Methods such
    as get_bounds() are therefore not available when using it.

    Parameters
    ----------
    data: list of list with values
        List of list of shape [[lat, lon], [lat, lon], etc.]
        When you use a custom callback you could add more values after the
        lat and lon. E.g. [[lat, lon, 'red'], [lat, lon, 'blue']]
    callback: string, optional
        A string representation of a valid Javascript function
        that will be passed each row in data. See the
        FasterMarkerCluster for an example of a custom callback.
    name : string, optional
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    icon_create_function : string, default None
        Override the default behaviour, making possible to customize
        markers colors and sizes.
    **kwargs
        Additional arguments are passed to Leaflet.markercluster options. See
        https://github.com/Leaflet/Leaflet.markercluster

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = (function(){
                {{ this.callback }}

                var data = {{ this.data|tojson }};
                var cluster = L.markerClusterGroup({{ this.options|tojson }});
                {%- if this.icon_create_function is not none %}
                cluster.options.iconCreateFunction =
                    {{ this.icon_create_function.strip() }};
                {%- endif %}

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var marker = callback(row);
                    marker.addTo(cluster);
                }

                cluster.addTo({{ this._parent.get_name() }});
                return cluster;
            })();
        {% endmacro %}"""
    )

    def __init__(
        self,
        data,
        callback=None,
        options=None,
        name=None,
        overlay=True,
        control=True,
        show=True,
        icon_create_function=None,
        **kwargs,
    ):
        if options is not None:
            kwargs.update(options)  # options argument is legacy
        super().__init__(
            name=name,
            overlay=overlay,
            control=control,
            show=show,
            icon_create_function=icon_create_function,
            **kwargs,
        )
        self._name = "FastMarkerCluster"
        data = if_pandas_df_convert_to_numpy(data)
        self.data = [
            [*validate_location(row[:2]), *row[2:]] for row in data  # noqa: E999
        ]

        if callback is None:
            self.callback = """
                var callback = function (row) {
                    var icon = L.AwesomeMarkers.icon();
                    var marker = L.marker(new L.LatLng(row[0], row[1]));
                    marker.setIcon(icon);
                    return marker;
                };"""
        else:
            self.callback = f"var callback = {callback};"
