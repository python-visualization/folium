    var legend = L.control({position: 'topright'});

    legend.onAdd = function (map) {var div = L.DomUtil.create('div', 'legend'); return div};

    legend.addTo(map);

    var x = d3.scale.linear()
    .domain([0, {{ lin_max }}])
    .range([0, 400]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("top")
        .tickSize(1)
        .tickValues({{ tick_labels }});

    var svg = d3.select(".legend.leaflet-control").append("svg")
        .attr("id", 'legend')
        .attr("width", 450)
        .attr("height", 40);

    var g = svg.append("g")
        .attr("class", "key")
        .attr("transform", "translate(25,16)");

    g.selectAll("rect")
        .data(color.range().map(function(d, i) {
          return {
            x0: i ? x(color.domain()[i - 1]) : x.range()[0],
            x1: i < color.domain().length ? x(color.domain()[i]) : x.range()[1],
            z: d
          };
        }))
      .enter().append("rect")
        .attr("height", 10)
        .attr("x", function(d) { return d.x0; })
        .attr("width", function(d) { return d.x1 - d.x0; })
        .style("fill", function(d) { return d.z; });

    g.call(xAxis).append("text")
        .attr("class", "caption")
        .attr("y", 21)
        .text('{{ caption }}');
