from copy import copy
from uuid import uuid4
from jinja2 import Template
from collections import OrderedDict

from branca.element import MacroElement, Figure, JavascriptLink

from folium.folium import Map


class DualMap(MacroElement):
    """Create two maps in the same window.

    Adding children to this objects adds them to both maps. You can access
    the individual maps with `DualMap.m1` and `DualMap.m2`.

    Uses the Leaflet plugin Sync: https://github.com/jieter/Leaflet.Sync

    Parameters
    ----------
    layout : {'horizontal', 'vertical'}
        Select how the two maps should be positioned. Either horizontal (left
        and right) or vertical (top and bottom).

    Examples
    --------
    >>> # DualMap accepts the same arguments as Map:
    >>> m = DualMap(location=(0, 0), tiles='cartodbpositron',  zoom_start=5)
    >>> # Add the same marker to both maps:
    >>> Marker((0, 0)).add_to(m)
    >>> # The individual maps are attributes called `m1` and `m2`:
    >>> Marker((0, 1)).add_to(m.m1)
    >>> LayerControl().add_to(m)
    >>> m.save('map.html')

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
        {{ this.m1.get_name() }}.sync({{ this.m2.get_name() }});
        {{ this.m2.get_name() }}.sync({{ this.m1.get_name() }});
        {% endmacro %}
    """)

    def __init__(self, location=None, layout='horizontal', **kwargs):
        super(DualMap, self).__init__()
        for key in ('width', 'height', 'left', 'top', 'position'):
            assert key not in kwargs, ('Argument {} cannot be used with '
                                       'DualMap.'.format(key))
        if layout not in ('horizontal', 'vertical'):
            raise ValueError('Undefined option for argument `layout`: {}. '
                             'Use either \'horizontal\' or \'vertical\'.'
                             .format(layout))
        width = '50%' if layout == 'horizontal' else '100%'
        height = '100%' if layout == 'horizontal' else '50%'
        self.m1 = Map(location=location, width=width, height=height,
                      left='0%', top='0%',
                      position='absolute', **kwargs)
        self.m2 = Map(location=location, width=width, height=height,
                      left='50%' if layout == 'horizontal' else '0%',
                      top='0%' if layout == 'horizontal' else '50%',
                      position='absolute', **kwargs)
        figure = Figure()
        figure.add_child(self.m1)
        figure.add_child(self.m2)
        # Important: add self to Figure last.
        figure.add_child(self)
        self.children_for_m2 = []

    def add_child(self, child, name=None, index=None):
        self.m1.add_child(child, name, index)
        self.children_for_m2.append(child)

    def _copy_item(self, item_original):
        """Return a recursive deep-copy of item where each copy has a new ID."""
        item = copy(item_original)
        item._id = uuid4().hex
        if hasattr(item, '_children') and len(item._children) > 0:
            children_new = OrderedDict()
            for subitem_original in item._children.values():
                subitem = self._copy_item(subitem_original)
                subitem._parent = item
                children_new[subitem.get_name()] = subitem
            item._children = children_new
        return item

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(JavascriptLink('https://rawgit.com/jieter/Leaflet.Sync/master/L.Map.Sync.js'),  # noqa
                                name='Leaflet.Sync')

        super(DualMap, self).render(**kwargs)

        for child in self.children_for_m2:
            child_copy = self._copy_item(child)
            self.m2.add_child(child_copy)
            # m2 has already been rendered, so render the child here.
            child_copy.render()