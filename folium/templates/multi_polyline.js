var latLngs = [
{% for location in locations %}
    [
    {% for loc in location %}
        [{{ loc[0] }}, {{ loc[1] }}],
    {% endfor %}
    ],
{% endfor %}];

var {{ multiline }} = L.multiPolyline(latLngs,{
{% if options.color != None %}color: '{{ options.color }}',{% endif %}
{% if options.weight != None %}weight: {{ options.weight }},{% endif %}
{% if options.opacity != None %}opacity: {{ options.opacity }},{% endif %}
});
