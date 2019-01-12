from __future__ import (absolute_import, division, print_function)

import pytest

from folium.utilities import camelize, deep_copy, get_obj_in_upper_tree
from folium import Map, FeatureGroup, Marker, Popup


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


def test_get_obj_in_upper_tree():
    m = Map()
    fg = FeatureGroup().add_to(m)
    marker = Marker(location=(0, 0)).add_to(fg)
    assert get_obj_in_upper_tree(marker, FeatureGroup) is fg
    assert get_obj_in_upper_tree(marker, Map) is m
    # The search should only go up, not down:
    with pytest.raises(ValueError):
        assert get_obj_in_upper_tree(fg, Marker)
    with pytest.raises(ValueError):
        assert get_obj_in_upper_tree(marker, Popup)
