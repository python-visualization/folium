# -*- coding: utf-8 -*-

from branca.element import CssLink, Figure, JavascriptLink, MacroElement

from folium.utilities import parse_options

from jinja2 import Template


class MeasureControl(MacroElement):
    """ Add a measurement widget on the map.

    Parameters
    ----------
    position: str, default 'topright'
        Location of the widget.
    primary_length_unit: str, default 'meters'
    secondary_length_unit: str, default 'miles'
    primary_area_unit: str, default 'sqmeters'
    secondary_area_unit: str, default 'acres'

    See https://github.com/ljagis/leaflet-measure for more information.

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = new L.Control.Measure(
                {{ this.options|tojson }});
            {{this._parent.get_name()}}.addControl({{this.get_name()}});

        {% endmacro %}
        """)  # noqa

    def __init__(self, position='topright', primary_length_unit='meters',
                 secondary_length_unit='miles', primary_area_unit='sqmeters',
                 secondary_area_unit='acres', **kwargs):

        super(MeasureControl, self).__init__()
        self._name = 'MeasureControl'

        self.options = parse_options(
            position=position,
            primary_length_unit=primary_length_unit,
            secondary_length_unit=secondary_length_unit,
            primary_area_unit=primary_area_unit,
            secondary_area_unit=secondary_area_unit,
            **kwargs
        )

    def render(self, **kwargs):
        super(MeasureControl, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://rawcdn.githack.com/ljagis/leaflet-measure/2.1.7/dist/leaflet-measure.js'))  # noqa

        figure.header.add_child(
            CssLink('https://rawcdn.githack.com/ljagis/leaflet-measure/2.1.7/dist/leaflet-measure.css'))  # noqa
