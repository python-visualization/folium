var latLngs = [{% for loc in locations %} [{{ loc[0] }}, {{ loc[1] }}], {% endfor %}];
var {{ line }} = L.polyline(latLngs,{
{% if options.color != None %}color: '{{ options.color }}',{% endif %}
{% if options.weight != None %}weight: {{ options.weight }},{% endif %}
{% if options.opacity != None %}opacity: {{ options.opacity }},{% endif %}
});
