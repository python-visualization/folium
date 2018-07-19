# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class MousePosition(MacroElement):
    """
    Adds a mouse position widget on the map.

    Parameters
    ----------
    position: location of the widget
        default is 'bottomright'.

    CONVERTED TO PYTHON FROM:

    https://github.com/ardhi/Leaflet.MousePosition

    With the MIT License as below:

    Copyright 2012 Ardhi Lukianto

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new L.Control.MousePosition(
            {{ this.options }});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
        """)  # noqa

    def __init__(self, position='bottomright', separator=' : ', emptyString='Unavailable', lngFirst=False, numDigits=5,
                 lngFormatter=None, latFormatter=None, prefix=""):
        """Coordinate, linear, and area measure control"""
        super(MousePosition, self).__init__()
        self._name = 'MousePosition'

        options = {
            'position': position,
            'separator': separator,
            'emptyString': emptyString,
            'lngFirst': lngFirst,
            'numDigits': numDigits,
            'lngFormatter': lngFormatter,
            'latFormatter': latFormatter,
            'prefix': prefix,
        }
        self.options = json.dumps(options)

    def render(self, **kwargs):
        super(MousePosition, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.rawgit.com/ardhi/Leaflet.MousePosition/c32f1c84/src/L.Control.MousePosition.js'))  # noqa

        figure.header.add_child(
            CssLink('https://cdn.rawgit.com/ardhi/Leaflet.MousePosition/c32f1c84/src/L.Control.MousePosition.css'))  # noqa
