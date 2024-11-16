from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.utilities import parse_options


class OverlappingMarkerSpiderfier(JSCSSMixin, Layer):
    """A plugin that handles overlapping markers by spreading them into a spider-like pattern.

    This plugin uses the OverlappingMarkerSpiderfier-Leaflet library to manage markers
    that are close to each other or overlap. When clicked, the overlapping markers
    spread out in a spiral pattern, making them easier to select individually.

    Parameters
    ----------
    markers : list, optional
        List of markers to be managed by the spiderfier
    name : string, optional
        Name of the layer control
    overlay : bool, default True
        Whether the layer will be included in LayerControl
    control : bool, default True
        Whether the layer will be included in LayerControl
    show : bool, default True
        Whether the layer will be shown on opening
    options : dict, optional
        Additional options to be passed to the OverlappingMarkerSpiderfier instance
        See https://github.com/jawj/OverlappingMarkerSpiderfier-Leaflet for available options

    Example
    -------
    >>> markers = [marker1, marker2, marker3]  # Create some markers
    >>> spiderfier = OverlappingMarkerSpiderfier(
    ...     markers=markers, keepSpiderfied=True, nearbyDistance=20
    ... )
    >>> spiderfier.add_to(m)  # Add to your map
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = (function () {
            var layerGroup = L.layerGroup();

            try {
                var oms = new OverlappingMarkerSpiderfier(
                    {{ this._parent.get_name() }},
                    {{ this.options|tojson }}
                );

                var popup = L.popup({
                    offset: L.point(0, -30)
                });

                oms.addListener('click', function(marker) {
                    var content;
                    if (marker.options && marker.options.options && marker.options.options.desc) {
                        content = marker.options.options.desc;
                    } else if (marker._popup && marker._popup._content) {
                        content = marker._popup._content;
                    } else {
                        content = "";
                    }

                    if (content) {
                        popup.setContent(content);
                        popup.setLatLng(marker.getLatLng());
                        {{ this._parent.get_name() }}.openPopup(popup);
                    }
                });

                oms.addListener('spiderfy', function(markers) {
                    {{ this._parent.get_name() }}.closePopup();
                });

                {% for marker in this.markers %}
                var {{ marker.get_name() }} = L.marker(
                    {{ marker.location|tojson }},
                    {{ marker.options|tojson }}
                );

                {% if marker.popup %}
                {{ marker.get_name() }}.bindPopup({{ marker.popup.get_content()|tojson }});
                {% endif %}

                oms.addMarker({{ marker.get_name() }});
                layerGroup.addLayer({{ marker.get_name() }});
                {% endfor %}
            } catch (error) {
                console.error('Error in OverlappingMarkerSpiderfier initialization:', error);
            }

            return layerGroup;
        })();
        {% endmacro %}

        """
    )

    default_js = [
        (
            "overlappingmarkerjs",
            "https://cdnjs.cloudflare.com/ajax/libs/OverlappingMarkerSpiderfier-Leaflet/0.2.6/oms.min.js",
        )
    ]

    def __init__(
        self,
        markers=None,
        name=None,
        overlay=True,
        control=True,
        show=True,
        options=None,
        **kwargs,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "OverlappingMarkerSpiderfier"

        self.markers = markers or []

        default_options = {
            "keepSpiderfied": True,
            "nearbyDistance": 20,
            "legWeight": 1.5,
        }
        if options:
            default_options.update(options)

        self.options = parse_options(**default_options, **kwargs)
