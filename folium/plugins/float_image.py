# -*- coding: utf-8 -*-
"""
FloatImage plugin
-----------------

Adds a floating image in HTML canvas on top of the map.
"""
from jinja2 import Template

from branca.element import MacroElement


class FloatImage(MacroElement):
    def __init__(self, image, bottom=75, left=75):
        """Adds a floating image in HTML canvas on top of the map."""
        super(FloatImage, self).__init__()
        self._name = 'FloatImage'
        self.image = image
        self.bottom = bottom
        self.left = left

        self._template = Template("""
            {% macro header(this,kwargs) %}
                <style>
                    #{{this.get_name()}} {
                        position:absolute;
                        bottom:{{this.bottom}}%;
                        left:{{this.left}}%;
                        }
                </style>
            {% endmacro %}

            {% macro html(this,kwargs) %}
            <img id="{{this.get_name()}}" alt="float_image"
                 src="{{ this.image }}"
                 style="z-index: 999999">
            </img>
            {% endmacro %}
            """)
