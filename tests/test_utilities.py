from __future__ import (absolute_import, division, print_function)

from folium.utilities import camelize, deep_copy
from folium import Map, FeatureGroup, Marker


def test_camelize():
    assert camelize('variable_name') == 'variableName'
    assert camelize('variableName') == 'variableName'
    assert camelize('name') == 'name'
    assert camelize('very_long_variable_name') == 'veryLongVariableName'


def test_deep_copy():
    m = Map()
    fg = FeatureGroup().add_to(m)
    Marker(location=(0, 0)).add_to(fg)
    m_copy = deep_copy(m)

    def check(item, item_copy):
        assert type(item) is type(item_copy)
        assert item._name == item_copy._name
        for attr in item.__dict__.keys():
            if not attr.startswith('_'):
                assert getattr(item, attr) == getattr(item_copy, attr)
        assert item is not item_copy
        assert item._id != item_copy._id
        for child, child_copy in zip(item._children.values(),
                                     item_copy._children.values()):
            check(child, child_copy)

    check(m, m_copy)
