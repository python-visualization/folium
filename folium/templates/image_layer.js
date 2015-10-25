var {{ this.get_name() }} = L.imageOverlay(
     '{{ image_url }}',
     {{ image_bounds }}
     {% if image_opacity %}, {"opacity" : {{ image_opacity }} } {% endif %}
     ).addTo({{ this._parent.get_name() }});
