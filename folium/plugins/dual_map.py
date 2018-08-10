from copy import copy
from uuid import uuid4
from jinja2 import Template
from collections import OrderedDict

from branca.element import MacroElement, Figure, JavascriptLink

from folium.folium import Map


class DualMap(MacroElement):
    """

    https://github.com/jieter/Leaflet.Sync

    """
    _template = Template("""
        {% macro script(this, kwargs) %}
        {{ this.m1.get_name() }}.sync({{ this.m2.get_name() }});
        {{ this.m2.get_name() }}.sync({{ this.m1.get_name() }});

        {% endmacro %}
    """)

    def __init__(self, location=None, **kwargs):
        super(DualMap, self).__init__()
        self.m1 = Map(location=location, width='50%', height='100%',
                      left='0%', top='0%', position='relative', **kwargs)
        self.m2 = Map(location=location, width='50%', height='100%',
                      left='50%', top='0%', position='absolute', **kwargs)
        figure = Figure()
        figure.add_child(self.m1)
        figure.add_child(self.m2)
        figure.add_child(self)
        self.children_unofficial = []

    def add_child(self, child, name=None, index=None):
        self.m1.add_child(child, name, index)
        self.children_unofficial.append(child)

    def _copy_item(self, item):
        item = copy(item)
        item._id = uuid4().hex
        children_new = OrderedDict()
        if hasattr(item, '_children') and len(item._children) > 0:
            for subitem in item._children.values():
                subitem_copy = self._copy_item(subitem)
                subitem_copy._parent = item
                children_new[subitem_copy.get_name()] = subitem_copy
        item._children = children_new
        return item

    def prerender(self):
        for child in self.children_unofficial:
            self.m2.add_child(self._copy_item(child))

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(JavascriptLink('https://rawgit.com/jieter/Leaflet.Sync/master/L.Map.Sync.js'),  # noqa
                                name='Leaflet.Sync')

        super(DualMap, self).render(**kwargs)
