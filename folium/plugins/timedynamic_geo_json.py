"""
module containing the class TimeDynamicGeoJson, which can be used to 
create choropleth maps with a time slider. 
"""
from jinja2 import Template
from branca.element import JavascriptLink, Figure
from folium.features import GeoJson


class TimeDynamicGeoJson(GeoJson):
    """
    Creates a GeoJson object for plotting into a Map.

    Parameters
    ----------
    data: file, dict or str.
        The GeoJSON data you want to plot.
        * If file, then data will be read in the file and fully
        embedded in Leaflet's JavaScript.
        * If dict, then data will be converted to JSON and embedded
        in the JavaScript.
        * If str, then data will be passed to the JavaScript as-is.
    style_function: function, default None
        A function mapping a GeoJson Feature to a style dict.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls
    smooth_factor: float, default None
        How much to simplify the polyline on each zoom level. More means
        better performance and smoother look, and less means more accurate
        representation. Leaflet defaults to 1.0.

    Examples
    --------
    >>> # Providing file that shall be embedded.
    >>> GeoJson(open('foo.json'))
    >>> # Providing filename that shall not be embedded.
    >>> GeoJson('foo.json')
    >>> # Providing dict.
    >>> GeoJson(json.load(open('foo.json')))
    >>> # Providing string.
    >>> GeoJson(open('foo.json').read())

    >>> # Provide a style_function that color all states green but Alabama.
    >>> style_function = lambda x: {'fillColor': '#0000ff' if
    ...                             x['properties']['name']=='Alabama' else
    ...                             '#00ff00'}
    >>> GeoJson(geojson, style_function=style_function)

    """
    def __init__(self, data, styledict, **kwargs):
        super(TimeDynamicGeoJson, self).__init__(data, **kwargs)
        assert isinstance(styledict, dict), 'styledict must be a dictionary'
        for val in styledict.values():
            assert isinstance(val, dict), 'each item in styledict must be a dictionary'

        self.styledict = styledict

        # make set of timestamps
        self.timestamps = set()
        for feature in self.styledict.values():
            self.timestamps.update(set(feature.keys()))
        self.timestamps = sorted(list(self.timestamps))

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                
                var timestamps = {{ this.timestamps }};
                var styledict = {{ this.styledict }};
                var current_timestamp = timestamps[0];

                // insert time slider
                d3.select("body").insert("p", ":first-child").append("input")   
                    .attr("type", "range")
                    .attr("width", "100px")
                    .attr("min", 0)
                    .attr("max", timestamps.length - 1)
                    .attr("value", 0)
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
                            d3.selectAll('#feature-'+feature_id).attr('fill', fillColor).style('fill-opacity', opacity);
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

                var {{this.get_name()}} = L.geoJson(
                    {% if this.embed %}{{this.style_data()}}{% else %}"{{this.data}}"{% endif %}
                    {% if this.smooth_factor is not none or this.highlight %}
                        , {
                        {% if this.smooth_factor is not none  %}
                            smoothFactor:{{this.smooth_factor}}
                        {% endif %}

                        {% if this.highlight %}
                            {% if this.smooth_factor is not none  %}
                            ,
                            {% endif %}
                            onEachFeature: {{this.get_name()}}_onEachFeature
                        {% endif %}
                        }
                    {% endif %}
                    ).addTo({{this._parent.get_name()}}
                );
               
        	{{this.get_name()}}.setStyle(function(feature) {feature.properties.style;});
                
                {{ this.get_name() }}.eachLayer(function (layer) {
                    layer._path.id = 'feature-' + layer.feature.id;
                    });

                d3.selectAll('path').attr('stroke', 'white').attr('stroke-width', 0.8).attr('stroke-dasharray', '5,5').attr('fill-opacity', 0);
                fill_map();
            
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(TimeDynamicGeoJson, self).render(**kwargs)
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        figure.header.add_child(JavascriptLink('http://d3js.org/d3.v4.min.js'))  # noqa
