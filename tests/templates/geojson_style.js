function {{ style }}(feature) {
    return {
        {%- if quantize_fill %}
        fillColor: {{ quantize_fill }},
        {%- else %}
        fillColor: '{{ fill_color }}',
        {%- endif %}
        weight: {{ line_weight }},
        opacity: {{ line_opacity }},
        color: '{{ line_color }}',
        fillOpacity: {{ fill_opacity }}
    };
}