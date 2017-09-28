from ..map import Layer
import json
from jinja2 import Template

from branca.utilities import none_min, none_max, iter_points
from six import text_type, binary_type


class TimeDynamicGeoJson(Layer):
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
    def __init__(self, data, styledict, style_function=None, name=None,
                 overlay=True, control=True, smooth_factor=None,
                 highlight_function=None):
        super(TimeDynamicGeoJson, self).__init__(name=name, overlay=overlay,
                                      control=control)
        self._name = 'GeoJson'
        if hasattr(data, 'read'):
            self.embed = True
            self.data = json.load(data)
        elif isinstance(data, dict):
            self.embed = True
            self.data = data
        elif isinstance(data, text_type) or isinstance(data, binary_type):
            if data.lstrip()[0] in '[{':  # This is a GeoJSON inline string
                self.embed = True
                self.data = json.loads(data)
            else:  # This is a filename
                self.embed = False
                self.data = data
        elif data.__class__.__name__ in ['GeoDataFrame', 'GeoSeries']:
            self.embed = True
            if hasattr(data, '__geo_interface__'):
                # We have a GeoPandas 0.2 object.
                self.data = json.loads(json.dumps(data.to_crs(epsg='4326').__geo_interface__))  # noqa
            elif hasattr(data, 'columns'):
                # We have a GeoDataFrame 0.1
                self.data = json.loads(data.to_crs(epsg='4326').to_json())
            else:
                msg = 'Unable to transform this object to a GeoJSON.'
                raise ValueError(msg)
        else:
            raise ValueError('Unhandled object {!r}.'.format(data))

        self.styledict = styledict
       
        # make set of timestamps
        self.timestamps = set()
        for feature in self.styledict.values():
            self.timestamps.update(set(feature.keys()))
        self.timestamps = sorted(list(self.timestamps))

        if style_function is None:
            def style_function(x):
                return {}

        self.style_function = style_function

        self.highlight = highlight_function is not None

        if highlight_function is None:
            def highlight_function(x):
                return {}

        self.highlight_function = highlight_function

        self.smooth_factor = smooth_factor

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
            """)  # noqa
  
    def style_data(self):
        """
        Applies `self.style_function` to each feature of `self.data` and
        returns a corresponding JSON output.

        """
        if 'features' not in self.data.keys():
            # Catch case when GeoJSON is just a single Feature or a geometry.
            if not (isinstance(self.data, dict) and 'geometry' in self.data.keys()):  # noqa
                # Catch case when GeoJSON is just a geometry.
                self.data = {'type': 'Feature', 'geometry': self.data}
            self.data = {'type': 'FeatureCollection', 'features': [self.data]}

        for feature in self.data['features']:
            feature.setdefault('properties', {}).setdefault('style', {}).update(self.style_function(feature))  # noqa
            feature.setdefault('properties', {}).setdefault('highlight', {}).update(self.highlight_function(feature))  # noqa
        return json.dumps(self.data, sort_keys=True)

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]

        """
        if not self.embed:
            raise ValueError('Cannot compute bounds of non-embedded GeoJSON.')

        if 'features' not in self.data.keys():
            # Catch case when GeoJSON is just a single Feature or a geometry.
            if not (isinstance(self.data, dict) and 'geometry' in self.data.keys()):  # noqa
                # Catch case when GeoJSON is just a geometry.
                self.data = {'type': 'Feature', 'geometry': self.data}
            self.data = {'type': 'FeatureCollection', 'features': [self.data]}

        bounds = [[None, None], [None, None]]
        for feature in self.data['features']:
            for point in iter_points(feature.get('geometry', {}).get('coordinates', {})):  # noqa
                bounds = [
                    [
                        none_min(bounds[0][0], point[1]),
                        none_min(bounds[0][1], point[0]),
                        ],
                    [
                        none_max(bounds[1][0], point[1]),
                        none_max(bounds[1][1], point[0]),
                        ],
                    ]
        return bounds
