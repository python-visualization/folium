from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.features import GeoJson
from folium.map import Layer


class TimeSliderChoropleth(JSCSSMixin, Layer):
    """
    Creates a TimeSliderChoropleth plugin to append into a map with Map.add_child.

    Parameters
    ----------
    data: str
        geojson string
    styledict: dict
        A dictionary where the keys are the geojson feature ids and the values are
        dicts of `{time: style_options_dict}`
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    init_timestamp: int, default 0
        Initial time-stamp index on the slider. Must be in the range
        `[-L, L-1]`, where `L` is the maximum number of time stamps in
        `styledict`. For example, use `-1` to initialize the slider to the
        latest timestamp.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var timestamps = {{ this.timestamps|tojson }};
            var styledict = {{ this.styledict|tojson }};
            var current_timestamp = timestamps[{{ this.init_timestamp }}];
            // insert time slider
            d3.select("body").insert("p", ":first-child").append("input")
                .attr("type", "range")
                .attr("width", "100px")
                .attr("min", 0)
                .attr("max", timestamps.length - 1)
                .attr("value", {{ this.init_timestamp }})
                .attr("id", "slider")
                .attr("step", "1")
                .style('align', 'center');

            // insert time slider output BEFORE time slider (text on top of slider)
            d3.select("body").insert("p", ":first-child").append("output")
                .attr("width", "100")
                .attr("id", "slider-value")
                .style('font-size', '18px')
                .style('text-align', 'center')
                .style('font-weight', '500%');

            var datestring = new Date(parseInt(current_timestamp)*1000).toDateString();
            d3.select("output#slider-value").text(datestring);

            fill_map = function(){
                for (var feature_id in styledict){
                    let style = styledict[feature_id]//[current_timestamp];
                    var fillColor = 'white';
                    var opacity = 0;
                    if (current_timestamp in style){
                        fillColor = style[current_timestamp]['color'];
                        opacity = style[current_timestamp]['opacity'];
                        d3.selectAll('#feature-'+feature_id
                        ).attr('fill', fillColor)
                        .style('fill-opacity', opacity);
                    }
                }
            }

            d3.select("#slider").on("input", function() {
                current_timestamp = timestamps[this.value];
                var datestring = new Date(parseInt(current_timestamp)*1000).toDateString();
                d3.select("output#slider-value").text(datestring);
                fill_map();
            });

            {% if this.highlight %}
                {{this.get_name()}}_onEachFeature = function onEachFeature(feature, layer) {
                    layer.on({
                        mouseout: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            var opacity = styledict[e.target.feature.id][current_timestamp]['opacity'];
                            d3.selectAll('#feature-'+e.target.feature.id).style('fill-opacity', opacity);
                        }
                    },
                        mouseover: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            d3.selectAll('#feature-'+e.target.feature.id).style('fill-opacity', 1);
                        }
                    },
                        click: function(e) {
                            {{this._parent.get_name()}}.fitBounds(e.target.getBounds());
                    }
                    });
                };
            {% endif %}

            var {{ this.get_name() }} = L.geoJson(
                    {{ this.data|tojson }}
            ).addTo({{ this._parent.get_name() }});

            {{ this.get_name() }}.setStyle(function(feature) {
                if (feature.properties.style !== undefined){
                    return feature.properties.style;
                }
                else{
                    return "";
                }
            });

            function onOverlayAdd(e) {
                {{ this.get_name() }}.eachLayer(function (layer) {
                    layer._path.id = 'feature-' + layer.feature.id;
                });

                d3.selectAll('path')
                .attr('stroke', 'white')
                .attr('stroke-width', 0.8)
                .attr('stroke-dasharray', '5,5')
                .attr('fill-opacity', 0);

                fill_map();
            }
            {{ this._parent.get_name() }}.on('overlayadd', onOverlayAdd);

            onOverlayAdd(); // fill map as layer is loaded
        {% endmacro %}
        """
    )

    default_js = [("d3v4", "https://d3js.org/d3.v4.min.js")]

    def __init__(
        self,
        data,
        styledict,
        name=None,
        overlay=True,
        control=True,
        show=True,
        init_timestamp=0,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self.data = GeoJson.process_data(GeoJson({}), data)

        if not isinstance(styledict, dict):
            raise ValueError(
                f"styledict must be a dictionary, got {styledict!r}"
            )  # noqa
        for val in styledict.values():
            if not isinstance(val, dict):
                raise ValueError(
                    f"Each item in styledict must be a dictionary, got {val!r}"
                )  # noqa

        # Make set of timestamps.
        timestamps = set()
        for feature in styledict.values():
            timestamps.update(set(feature.keys()))
        try:
            timestamps = sorted(timestamps, key=int)
        except (TypeError, ValueError):
            timestamps = sorted(timestamps)

        self.timestamps = timestamps
        self.styledict = styledict
        assert (
            -len(timestamps) <= init_timestamp < len(timestamps)
        ), "init_timestamp must be in the range [-{}, {}) but got {}".format(
            len(timestamps), len(timestamps), init_timestamp
        )
        if init_timestamp < 0:
            init_timestamp = len(timestamps) + init_timestamp
        self.init_timestamp = init_timestamp
