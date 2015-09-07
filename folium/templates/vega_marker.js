var {{vega}} = $('<div id="{{vega}}" ></div>')[0];
     {{popup}}.setContent({{vega}});

{{marker}}.bindPopup({{popup}});

vega_parse({{vega_json}},{{vega}});