# -*- coding: utf-8 -*-
"""
Crossfilter
------

Crossfilter.
"""
from jinja2 import Template
import json

#from .utilities import color_brewer, _parse_size, legend_scaler, _locations_mirror, _locations_tolist, write_png,\
#    image_to_url
#from .six import text_type, binary_type

from folium.element import Figure, JavascriptLink, CssLink, Div, MacroElement
from folium.map import FeatureGroup
#from .map import Map, TileLayer, Icon, Marker, Popup

class Crossfilter(Div):
    def __init__(self, data, **kwargs):
        """Create a Crossfilter

        Returns
        -------
        Folium Crossfilter Object

        """
        super(Crossfilter, self).__init__(**kwargs)
        self._name = 'Crossfilter'

        self.data = data

        self.add_children(MacroElement("""
            {% macro script(this, kwargs) %}
                var {{this._parent.get_name()}} = {};
                {{this._parent.get_name()}}.data = {{this._parent.data}};
                {{this._parent.get_name()}}.crossfilter = crossfilter({{this._parent.get_name()}}.data);
                {{this._parent.get_name()}}.allDim = {{this._parent.get_name()}}.crossfilter.dimension(
                    function(d) {return d;});
            {% endmacro %}
            """))

        self._template = Template(u"""
            {% macro header(this, kwargs) %}
                <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                </style>
            {% endmacro %}
            {% macro html(this, kwargs) %}
                <div id="{{this.get_name()}}">
                    {{this.html.render(**kwargs)}}
                </div>
            {% endmacro %}
            {% macro script(this, kwargs) %}
               dc.renderAll();
            {% endmacro %}
        """)
    def render(self,**kwargs):
        super(Crossfilter,self).render(**kwargs)

        figure = self._parent.get_root()
        assert isinstance(figure,Figure), ("You cannot render this Element "
            "if it's not in a Figure.")

        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/dc/1.7.5/dc.css"),
            name='dcjs_css')
        figure.header.add_children(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css"),
            name='leaflet_css')
        figure.header.add_children(
            CssLink("https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"),
            name='bootstrap_css')

        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"),
            name='d3js')
        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.12/crossfilter.min.js"),
            name='crossfilterjs')
        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-beta.20/dc.js"),
            name='dcjs')
        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"),
            name='leaflet')
        figure.header.add_children(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"),
            name='underscorejs')

class PieFilter(Div):
    def __init__(self, crossfilter, column, name="", width=150, height=150, inner_radius=20,
                 order=None, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(PieFilter, self).__init__(width=width, height=height, **kwargs)
        self._name = 'PieFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.name = name
        self.width = width
        self.height = height
        self.inner_radius = inner_radius
        self.order = order

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};

            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {return d["{{this.column}}"];});
            document.getElementById("{{this.get_name()}}").innerHTML =
                '<h4>{{this.name}} <small><a id="{{this.get_name()}}-reset">reset</a></small></h4>'
                + '<div id="{{this.get_name()}}-chart" class="dc-chart"></div>';

            {{this.get_name()}}.chart = dc.pieChart('#{{this.get_name()}}-chart')
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group().reduceCount())
                .innerRadius({{this.inner_radius}})
                {% if this.order %}.ordering(function (d) {
                    var out = null;
                    var order={{this.order}};
                    for (var j=0;j<order.length;j++) {
                        if (order[j]==d.key) {out = 1+j;}
                        }
                    return out;}){% endif %};
            d3.selectAll('#{{this.get_name()}}-reset').on('click',function () {
                {{this.get_name()}}.chart.filterAll();
                dc.redrawAll();
                });
        {% endmacro %}
        """)

class BarFilter(Div):
    def __init__(self, crossfilter, column, width=150, height=150, bar_padding=0.1,
                 domain=None, groupby=None, xlabel="", ylabel="", margins=None,
                 xticks=None, time_format=None, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(BarFilter, self).__init__(**kwargs)
        self._name = 'BarFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.width=width
        self.height=height
        self.bar_padding=bar_padding
        self.domain=json.dumps(domain)
        self.groupby=groupby
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.margins=json.dumps(margins)
        self.xticks=json.dumps(xticks)
        self.time_format=time_format

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {
                domain : {{this.domain}},
                groupby : {{this.groupby}},
                xAxisTickValues : {{this.xticks}},
                };
            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {
                    return Math.floor(
                        (d["{{this.column}}"]-{{this.get_name()}}.domain[0])/{{this.get_name()}}.groupby)
                        +{{this.get_name()}}.domain[0]/{{this.get_name()}}.groupby;
                    });
            {{this.get_name()}}.ticks = [];
            for (var j=0; j<{{this.get_name()}}.xAxisTickValues.length; j++) {
                {{this.get_name()}}.ticks[j] = {{this.get_name()}}.xAxisTickValues[j]/{{this.get_name()}}.groupby;
                }

            dc.barChart("#{{this.get_name()}}")
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group().reduceCount())
                .x(d3.scale.linear().domain([
                    {{this.get_name()}}.domain[0]/{{this.get_name()}}.groupby,
                    {{this.get_name()}}.domain[1]/{{this.get_name()}}.groupby,
                    ]))
                .elasticY(false)
                .centerBar(false)
                .barPadding({{this.bar_padding}})
                .xAxisLabel("{{this.xlabel}}")
                .yAxisLabel("{{this.ylabel}}")
                .margins({{this.margins}})
                .xAxis()
                  .tickValues({{this.get_name()}}.ticks)
                  .tickFormat(function(x){
                      {%if this.time_format %}
                      var dateformat = d3.time.format("{{this.time_format}}");
                      return dateformat(new Date(x*{{this.get_name()}}.groupby));
                      {% else %}
                      return x*{{this.get_name()}}.groupby;
                      {% endif %}
                      });
        {% endmacro %}
        """)

class FeatureGroupFilter(FeatureGroup):
    def __init__(self, crossfilter, name=None, fit_bounds=False, **kwargs):
        """
        """
        super(FeatureGroupFilter, self).__init__(**kwargs)
        self._name = 'FeatureGroupFilter'

        self.tile_name = name if name is not None else self.get_name()

        self.crossfilter = crossfilter
        self.fit_bounds = fit_bounds

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.feature_group = new L.FeatureGroup();
            {{this.get_name()}}.updateFun = function() {
                this.feature_group.clearLayers();
                var dimVals = {{this.crossfilter.get_name()}}.allDim.top(Infinity)
                for (var i in dimVals) {
                var d = dimVals[i];
                    var marker = L.marker([d.lat, d.lng]);
                    marker.bindPopup(d.popup);
                    this.feature_group.addLayer(marker);
                    }
                {{this._parent.get_name()}}.addLayer(this.feature_group);
                {% if this.fit_bounds %}{{this._parent.get_name()}}
                    .fitBounds(this.feature_group.getBounds());{% endif %}
                }
            dc.dataTable('#foo')
               .dimension({{this.crossfilter.get_name()}}.allDim)
               .group(function (d) { return 'dc.js';})
               .on('renderlet', function (table) { {{this.get_name()}}.updateFun();});
            {{this.get_name()}}.updateFun();
        {% endmacro %}
        """)

class TableFilter(Div):
    def __init__(self, crossfilter, columns, sort_by=None, ascending=True, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(TableFilter, self).__init__(**kwargs)
        self._name = 'TableFilter'

        self.crossfilter = crossfilter
        self.columns = columns
        self.sort_by = sort_by
        self.ascending = ascending

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
        <table id="{{this.get_name()}}" class="{{this.class_}}">
            <thead>
                <tr class="header">
                {%for col in this.columns%}<th>{{col}}</th>{% endfor %}
                </tr>
            </thead>
        </table>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.dataTable = dc.dataTable('#{{this.get_name()}}');
            {{this.get_name()}}.dataTable
                .dimension({{this.crossfilter.get_name()}}.allDim)
                .group(function (d) { return 'dc.js extra line'; })
                .size(10)
                .columns([
                  {% for col in this.columns %}
                  function (d) { return d["{{col}}"]; },
                  {% endfor %}
                  ])
                {%if this.sort_by %}.sortBy(dc.pluck('{this.sort_by}'))
                {%if this.ascending %}.order(d3.ascending){% else %}.order(d3.descending){% endif %}
                {% endif %}
                .on('renderlet', function (table) {
                    table.select('tr.dc-table-group').remove();
                    });
        {% endmacro %}
        """)