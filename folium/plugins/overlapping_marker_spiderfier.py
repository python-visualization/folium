from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.map import Layer
from folium.utilities import parse_options


class OverlappingMarkerSpiderfier(JSCSSMixin, Layer):
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
