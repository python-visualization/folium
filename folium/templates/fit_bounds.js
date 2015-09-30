{% if autobounds %}
var autobounds = L.featureGroup({{ features }}).getBounds()
{% if not bounds %}
{% set bounds = "autobounds" %}
{% endif %}
{% endif %}
{% if bounds %}
{{this._parent.get_name()}}.fitBounds({{ bounds }},
    {{ fit_bounds_options }}
);
{% endif %}
