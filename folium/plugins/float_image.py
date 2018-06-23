# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from branca.element import MacroElement

from jinja2 import Template


class FloatImage(MacroElement):
    """Adds a floating image in HTML canvas on top of the map."""
    _template = Template("""
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

    def __init__(self, image, bottom=75, left=75):
        super(FloatImage, self).__init__()
        self._name = 'FloatImage'
        self.image = image
        self.bottom = bottom
        self.left = left
