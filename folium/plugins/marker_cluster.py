from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer, Marker
from folium.utilities import parse_options, validate_locations


class MarkerCluster(JSCSSMixin, Layer):
    """
    Provides Beautiful Animated Marker Clustering functionality for maps.

    Parameters
    ----------
    locations: list of list or array of shape (n, 2).
        Data points of the form [[lat, lng]].
    popups: list of length n, default None
        Popup for each marker, either a Popup object or a string or None.
    icons: list of length n, default None
        Icon for each marker, either an Icon object or a string or None.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    icon_create_function : string, default None
        Override the default behaviour, making possible to customize
        markers colors and sizes.
    options : dict, default None
        A dictionary with options for Leaflet.markercluster. See
        https://github.com/Leaflet/Leaflet.markercluster for options.

    Example
    -------
    >>> icon_create_function = '''
    ...     function(cluster) {
    ...     return L.divIcon({html: '<b>' + cluster.getChildCount() + '</b>',
    ...                       className: 'marker-cluster marker-cluster-small',
    ...                       iconSize: new L.Point(20, 20)});
    ...     }
    ... '''

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.markerClusterGroup(
                {{ this.options|tojson }}
            );
            {%- if this.icon_create_function is not none %}
            {{ this.get_name() }}.options.iconCreateFunction =
                {{ this.icon_create_function.strip() }};
            {%- endif %}
        {% endmacro %}
        """
    )

    default_js = [
        (
            "markerclusterjs",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js",
        )
    ]

    default_css = [
        (
            "markerclustercss",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css",
        ),
        (
            "markerclusterdefaultcss",
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css",
        ),
    ]

    def __init__(
        self,
        locations=None,
        popups=None,
        icons=None,
        name=None,
        overlay=True,
        control=True,
        show=True,
        icon_create_function=None,
        options=None,
        **kwargs
    ):
        if options is not None:
            kwargs.update(options)  # options argument is legacy
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "MarkerCluster"

        if locations is not None:
            locations = validate_locations(locations)
            for i, location in enumerate(locations):
                self.add_child(
                    Marker(
                        location, popup=popups and popups[i], icon=icons and icons[i]
                    )
                )

        self.options = parse_options(**kwargs)
        if icon_create_function is not None:
            assert isinstance(icon_create_function, str)
        self.icon_create_function = icon_create_function
