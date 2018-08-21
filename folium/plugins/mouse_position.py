# -*- coding: utf-8 -*-

# CONVERTED TO PYTHON FROM: https://github.com/ardhi/Leaflet.MousePosition
# With the MIT License as below.

# Copyright 2012 Ardhi Lukianto

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class MousePosition(MacroElement):
    """

    Parameters
    ----------
    position : str, default 'bottomright'
        Location of the widget.

    separator : str, default ' : '
        Character used to separate latitude and longitude values.

    empty_string : str, default 'Unavailable'
       String to display when a value cannot be returned.

    lng_first : bool, default 'False'
        Set as True to display longitude before latitude.

    num_digits : int, default '5'
        Number of decimal places included in the displayed
        longitude and latitude decimal degree values.

    lng_formatter : str, default 'None'
        Set the format for the longitude values.

    lat_formatter : str, default 'None'
       Set the format for the latitude values.

    prefix : str, default ''
        String to display before the latitude and longitude values.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new L.Control.MousePosition(
            {{ this.options }});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
        """)  # noqa

    def __init__(self, position='bottomright', separator=' : ',
                 empty_string='Unavailable', lng_first=False,
                 num_digits=5, lng_formatter=None, lat_formatter=None,
                 prefix=""):
        
        super(MousePosition, self).__init__()
        self._name = 'MousePosition'

        options = {
            'position': position,
            'separator': separator,
            'empty_string': empty_string,
            'lng_first': lng_first,
            'num_digits': num_digits,
            'lng_formatter': lng_formatter,
            'lat_formatter': lat_formatter,
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
