from ..map import Layer
import json
from jinja2 import Template

from branca.element import MacroElement, Figure, JavascriptLink, CssLink
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
    def __init__(self, data, style_function=None, name=None,
                 overlay=True, control=True, smooth_factor=None,
                 highlight_function=None, feature_properties=None):
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
            // ------------------- inserted code for creating time slider --------------------------
            // ACTUALLY all of this should be moved to the template for GeoJson elements? 
            // The time slider must be inserted here, but ranges can be laoded dynamically
            // data, currently placed in feature_properties, can be fed to GeoJson constructor and assigned a name prefixed with geojson name
            // Then it will be possible to create a map with several geojson features, and select the active one from a LayerControl
            
            var normalization_constant = 5; // TO DO: set dynamically and change to colormap_min/max values for normalizing color range
            var feature_properties; // 
            var current_timestamp; // TO DO: variable is used by the geojson mouseon/out setters in GeoJson
                                   // It is not really necessary, since it should be possible to get value from slider element directly

            function set_feature_color(data, year){
                    d3.selectAll('.leaflet-interactive').attr("fill", '#fff').style('opacity', 0);
                    for (var feature_id in data[year]){
                        let color = parseFloat(data[year][feature_id]["total_score-mean"]) / normalization_constant;
                        d3.selectAll('#feature-'+feature_id).attr("fill", d3.interpolateReds(color)).style('opacity', 0.8);;
                    }
                    
                }

            function main(error, timestamps, data){
                if(error) { console.log(error); }
        
                d3.select("body").insert("p", ":first-child").append("input")   
                .attr("type", "range")
                .attr("min", 0)
                .attr("max", timestamps.length - 1)
                .attr("value", 0)
                .attr("id", "slider")
                .attr("step", "1");
                
                current_timestamp = timestamps[0];
                feature_properties = data;

                console.log('done');

                d3.select("#slider").on("input", function() {
                    let timestamp = timestamps[this.value];
                    console.log(timestamp);
                    set_feature_color(data, timestamp);
                    current_timestamp = timestamp;
                }); 

                set_feature_color(data, timestamps[0]);

            }

            d3.queue()
            .defer(d3.json, "timestamps.json")
            .defer(d3.json, "titties.json")
            .await(main);

            // ------------------------------------ end of inserted code ----------------------

            {% if this.highlight %}
                {{this.get_name()}}_onEachFeature = function onEachFeature(feature, layer) {
                    layer.on({
                        mouseout: function(e) {
                            if(e.target.feature.id in feature_properties[current_timestamp]){
                                var color = d3.interpolateReds(feature_properties[current_timestamp][e.target.feature.id]["total_score-mean"]/normalization_constant);
                                var opacity = feature_properties[current_timestamp][e.target.feature.id]["total_score-count"]
                                d3.selectAll('#feature-'+e.target.feature.id).attr("fill", color).style('opacity', 0.8);
                            }
                        },
                        mouseover: function(e) {
                            if(e.target.feature.id in feature_properties[current_timestamp]){
                                var color = d3.interpolateReds(feature_properties[current_timestamp][e.target.feature.id]["total_score-mean"]/normalization_constant);
                                d3.selectAll('#feature-'+e.target.feature.id).attr("fill", color).style('opacity', 1);
                            }
                        },
                        click: function(e) {
                            map_44086f5b1db7451089af63824a52efbf.fitBounds(e.target.getBounds());
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
                    ).addTo({{this._parent.get_name()}});
                {{this.get_name()}}.setStyle(function(feature) {return feature.properties.style;});

                {{ this.get_name() }}.eachLayer(function (layer) {
                    layer._path.id = 'feature-' + layer.feature.properties.id;
                    });

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
        print(self.data)
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