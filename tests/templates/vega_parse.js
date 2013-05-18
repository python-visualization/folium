function parse(spec, div) {

    vg.parse.spec(spec, function(chart) { chart({el:div}).update(); });

}