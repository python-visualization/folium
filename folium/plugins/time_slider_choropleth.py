from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.features import GeoJson
from folium.map import Layer


class TimeSliderChoropleth(JSCSSMixin, Layer):
    """
    Create a choropleth with a timeslider for timestamped data.

    Visualize timestamped data, allowing users to view the choropleth at
    different timestamps using a slider.

    Parameters
    ----------
    data: str
        geojson string
    styledict: dict
        A dictionary where the keys are the geojson feature ids and the values are
        dicts of `{time: style_options_dict}`
    date_options: str, default "ddd MMM DD YYYY"
        A format string to render the currently active time in the control.
    highlight: bool, default False
        Whether to show a visual effect on mouse hover and click.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    init_timestamp: int, default 0
        Initial time-stamp index on the slider. Must be in the range
        `[-L, L-1]`, where `L` is the maximum number of time stamps in
        `styledict`. For example, use `-1` to initialize the slider to the
        latest timestamp.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        {
            let timestamps = {{ this.timestamps|tojson }};
            let styledict = {{ this.styledict|tojson }};
            let current_timestamp = timestamps[{{ this.init_timestamp }}];

            function formatDate(date) {
               var newdate = new moment(date);
               return newdate.format({{this.date_format|tojson}});
            }

            let slider_body = d3.select("body").insert("div", "div.folium-map")
                .attr("id", "slider_{{ this.get_name() }}");
            $("#slider_{{ this.get_name() }}").hide();
            // insert time slider label
            slider_body.append("output")
                .attr("width", "100")
                .style('font-size', '18px')
                .style('text-align', 'center')
                .style('font-weight', '500%')
                .style('margin', '5px');
            // insert time slider
            slider_body.append("input")
                .attr("type", "range")
                .attr("width", "100px")
                .attr("min", 0)
                .attr("max", timestamps.length - 1)
                .attr("value", {{ this.init_timestamp }})
                .attr("step", "1")
                .style('align', 'center');

            let datestring = formatDate(parseInt(current_timestamp)*1000);
            d3.select("#slider_{{ this.get_name() }} > output").text(datestring);

            let fill_map = function(){
                for (var feature_id in styledict){
                    let style = styledict[feature_id]//[current_timestamp];
                    var fillColor = 'white';
                    var opacity = 0;
                    if (current_timestamp in style){
                        fillColor = style[current_timestamp]['color'];
                        opacity = style[current_timestamp]['opacity'];
                        d3.selectAll('#{{ this.get_name() }}-feature-'+feature_id
                        ).attr('fill', fillColor)
                        .style('fill-opacity', opacity);
                    }
                }
            }

            d3.select("#slider_{{ this.get_name() }} > input").on("input", function() {
                current_timestamp = timestamps[this.value];
                let datestring = formatDate(parseInt(current_timestamp)*1000);
                d3.select("#slider_{{ this.get_name() }} > output").text(datestring);
                fill_map();
            });

            let onEachFeature;
            {% if this.highlight %}
                 onEachFeature = function(feature, layer) {
                    layer.on({
                        mouseout: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            var opacity = styledict[e.target.feature.id][current_timestamp]['opacity'];
                            d3.selectAll('#{{ this.get_name() }}-feature-'+e.target.feature.id).style('fill-opacity', opacity);
                        }
                    },
                        mouseover: function(e) {
                        if (current_timestamp in styledict[e.target.feature.id]){
                            d3.selectAll('#{{ this.get_name() }}-feature-'+e.target.feature.id).style('fill-opacity', 1);
                        }
                    },
                        click: function(e) {
                            {{this._parent.get_name()}}.fitBounds(e.target.getBounds());
                    }
                    });
                };
            {% endif %}

            var {{ this.get_name() }} = L.geoJson(
                {{ this.data|tojson }},
                {onEachFeature: onEachFeature}
            );

            {{ this.get_name() }}.setStyle(function(feature) {
                if (feature.properties.style !== undefined){
                    return feature.properties.style;
                }
                else{
                    return "";
                }
            });

            let onOverlayAdd = function(e) {
                {{ this.get_name() }}.eachLayer(function (layer) {
                    layer._path.id = '{{ this.get_name() }}-feature-' + layer.feature.id;
                });

                $("#slider_{{ this.get_name() }}").show();

                d3.selectAll('path')
                .attr('stroke', '{{ this.stroke_color }}')
                .attr('stroke-width', {{ this.stroke_width }})
                .attr('stroke-dasharray', '5,5')
                .attr('stroke-opacity', {{ this.stroke_opacity }})
                .attr('fill-opacity', 0);

                fill_map();
            }
            {{ this.get_name() }}.on('add', onOverlayAdd);
            {{ this.get_name() }}.on('remove', function() {
                $("#slider_{{ this.get_name() }}").hide();
            })

            {%- if this.show %}
            {{ this.get_name() }}.addTo({{ this._parent.get_name() }});
            $("#slider_{{ this.get_name() }}").show();
            {%- endif %}
        }
        {% endmacro %}
        """
    )

    default_js = [
        ("d3v4", "https://d3js.org/d3.v4.min.js"),
        (
            "moment",
            "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js",
        ),
    ]

    def __init__(
        self,
        data,
        styledict,
        date_options: str = "ddd MMM DD YYYY",
        highlight: bool = False,
        name=None,
        overlay=True,
        control=True,
        show=True,
        init_timestamp=0,
        stroke_opacity=1,
        stroke_width=0.8,
        stroke_color="#FFFFFF",
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self.data = GeoJson.process_data(GeoJson({}), data)
        self.date_format = date_options
        self.highlight = highlight

        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color

        if not isinstance(styledict, dict):
            raise ValueError(f"styledict must be a dictionary, got {styledict!r}")

        for val in styledict.values():
            if not isinstance(val, dict):
                raise ValueError(
                    f"Each item in styledict must be a dictionary, got {val!r}"
                )

        # Make set of timestamps.
        timestamps_set = set()
        for feature in styledict.values():
            timestamps_set.update(set(feature.keys()))
        try:
            timestamps = sorted(timestamps_set, key=int)
        except (TypeError, ValueError):
            timestamps = sorted(timestamps_set)

        self.timestamps = timestamps
        self.styledict = styledict
        assert (
            -len(timestamps) <= init_timestamp < len(timestamps)
        ), f"init_timestamp must be in the range [-{len(timestamps)}, {len(timestamps)}) but got {init_timestamp}"
        if init_timestamp < 0:
            init_timestamp = len(timestamps) + init_timestamp
        self.init_timestamp = init_timestamp
