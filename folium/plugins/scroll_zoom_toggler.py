# -*- coding: utf-8 -*-
"""
ScrollZoomToggler plugin
------------------------

Adds a button to enable/disable zoom scrolling.
"""
from .template_plugin import TemplatePlugin

class ScrollZoomToggler(TemplatePlugin):
    """Adds a button to enable/disable zoom scrolling."""
    template = """
    {% set plugin_name = "ScrollZoomToggler" %}
    {% macro css(nb) %}
        #ScrollZoomToggler_{{nb}} {
                position:absolute;
                width:35px;
                bottom:10px;
                height:35px;
                left:10px;
                background-color:#fff;
                text-align:center;
                line-height:35px;
                vertical-align: middle;
                }
    {% endmacro %}

    {% macro html(nb) %}
        <img id="ScrollZoomToggler_{{nb}}" alt="scroll"
           src="https://cdnjs.cloudflare.com/ajax/libs/ionicons/1.5.2/png/512/arrow-move.png"
           onclick="toggleScroll()"></img>
    {% endmacro %}

    {% macro js(nb) %}
        {% if nb==0 %}
            map.scrollEnabled = true;

            var toggleScroll = function() {
                if (map.scrollEnabled) {
                    map.scrollEnabled = false;
                    map.scrollWheelZoom.disable();
                    }
                else {
                    map.scrollEnabled = true;
                    map.scrollWheelZoom.enable();
                    }
                };

            toggleScroll();
        {% endif %}
    {% endmacro %}
    """