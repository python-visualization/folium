{% macro script(this, kwargs) %}
    var {{this.get_name()}} = {};

    {%if this.color_range %}
    {{this.get_name()}}.color = d3.scale.threshold()
              .domain({{this.color_domain}})
              .range({{this.color_range}});
    {%else%}
    {{this.get_name()}}.color = d3.scale.threshold()
              .domain([{{ this.color_domain[0] }}, {{ this.color_domain[-1] }}])
              .range(['{{ this.fill_color }}', '{{ this.fill_color }}']);
    {%endif%}

    {{this.get_name()}}.x = d3.scale.linear()
              .domain([{{ this.color_domain[0] }}, {{ this.color_domain[-1] }}])
              .range([0, 400]);

    {{this.get_name()}}.legend = L.control({position: 'topright'});
    {{this.get_name()}}.legend.onAdd = function (map) {var div = L.DomUtil.create('div', 'legend'); return div};
    {{this.get_name()}}.legend.addTo({{this._parent.get_name()}});

    {{this.get_name()}}.xAxis = d3.svg.axis()
        .scale({{this.get_name()}}.x)
        .orient("top")
        .tickSize(1)
        .tickValues({{ this.tick_labels }});

    {{this.get_name()}}.svg = d3.select(".legend.leaflet-control").append("svg")
        .attr("id", 'legend')
        .attr("width", 450)
        .attr("height", 40);

    {{this.get_name()}}.g = {{this.get_name()}}.svg.append("g")
        .attr("class", "key")
        .attr("transform", "translate(25,16)");

    {{this.get_name()}}.g.selectAll("rect")
        .data({{this.get_name()}}.color.range().map(function(d, i) {
          return {
            x0: i ? {{this.get_name()}}.x({{this.get_name()}}.color.domain()[i - 1]) : {{this.get_name()}}.x.range()[0],
            x1: i < {{this.get_name()}}.color.domain().length ? {{this.get_name()}}.x({{this.get_name()}}.color.domain()[i]) : {{this.get_name()}}.x.range()[1],
            z: d
          };
        }))
      .enter().append("rect")
        .attr("height", 10)
        .attr("x", function(d) { return d.x0; })
        .attr("width", function(d) { return d.x1 - d.x0; })
        .style("fill", function(d) { return d.z; });

    {{this.get_name()}}.g.call({{this.get_name()}}.xAxis).append("text")
        .attr("class", "caption")
        .attr("y", 21)
        .text('{{ this.caption }}');
{% endmacro %}