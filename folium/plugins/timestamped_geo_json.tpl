{% macro header(nb) %}
    {% if nb==0 %}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>

        <!-- iso8601 -->
        <script type="text/javascript" src="https://raw.githubusercontent.com/nezasa/iso8601-js-period/master/iso8601.min.js"></script>

        <!-- leaflet.timedimension.min.js -->
        <script type="text/javascript" src="https://raw.githubusercontent.com/socib/Leaflet.TimeDimension/master/dist/leaflet.timedimension.min.js"></script>

        <!-- leaflet.timedimension.control.min.css -->
        <link rel="stylesheet" href="http://apps.socib.es/Leaflet.TimeDimension/dist/leaflet.timedimension.control.min.css" />
    {% endif %}
{% endmacro %}

{% macro js(nb,self) %}
    {% if nb==0 %}
        map.timeDimension = L.timeDimension();
        map.timeDimensionControl = L.control.timeDimension({
            position: 'bottomleft',
            autoPlay: {{'true' if self.auto_play else 'false'}},
            playerOptions: {transitionTime: {{self.transition_time}},loop: {{'true' if self.loop else 'false'}}}
            });
        map.addControl(map.timeDimensionControl);
    {% endif %}

    var tsgeojson_{{nb}} = L.timeDimension.layer.geoJson(L.geoJson({{self.data}}),
        {updateTimeDimension: true,addlastPoint: true}).addTo(map);
{% endmacro %}