var {{ this.get_name() }} = {
                        color_function : function(feature) {
                            return '{{ fill_color }}';
                            },
                        };

{{ this._parent.get_name() }}.setStyle(function (feature) {
    return {
        {%- if quantize_fill %}
        fillColor: {{ quantize_fill }},
        {%- else %}
        fillColor: {{ this.get_name() }}.color_function(feature),
        {%- endif %}
        weight: {{ line_weight }},
        opacity: {{ line_opacity }},
        color: '{{ line_color }}',
        fillOpacity: {{ fill_opacity }},
        dashArray: '{{ dash_array }}'
    };
});