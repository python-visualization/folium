# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from jinja2 import Template


class MeasureControl(MacroElement):
    """
    Adds a measurem widget on the map.

    Parameters
    ----------
    position: location of the widget
        default is 'topright'.

    primary_length_unit and secondary_length_unit: length units
         defaults are 'meters' and 'miles' respectively.

    primary_area_unit and secondary_area_unit: ara units
        defaults are 'sqmeters' and 'acres' respectively.

    See https://github.com/ljagis/leaflet-measure for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = new L.Control.Measure(
            {{ this.options }});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
        """)  # noqa

    def __init__(self, position='topright', primary_length_unit='meters',
                 secondary_length_unit='miles', primary_area_unit='sqmeters',
                 secondary_area_unit='acres'):
        """Coordinate, linear, and area measure control"""
        super(MeasureControl, self).__init__()
        self._name = 'MeasureControl'

        options = {
            'position': position,
            'primaryLengthUnit': primary_length_unit,
            'secondaryLengthUnit': secondary_length_unit,
            'primaryAreaUnit': primary_area_unit,
            'secondaryAreaUnit': secondary_area_unit,
        }
        self.options = json.dumps(options)

    def render(self, **kwargs):
        super(MeasureControl, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/ljagis/leaflet-measure/2.1.7/dist/leaflet-measure.js'))  # noqa

        figure.header.add_child(
            CssLink('https://rawcdn.githack.com/ljagis/leaflet-measure/2.1.7/dist/leaflet-measure.css'))  # noqa
