var {{ this.get_name() }} = L.multiPolyline({{locations}},
    {
{% if options.color != None %}color: '{{ options.color }}',{% endif %}
{% if options.weight != None %}weight: {{ options.weight }},{% endif %}
{% if options.opacity != None %}opacity: {{ options.opacity }},{% endif %}
});
