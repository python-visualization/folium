from __future__ import (absolute_import, division, print_function)

import pytest

from folium.utilities import camelize, get_obj_in_upper_tree
from folium import Map, FeatureGroup, Marker, Popup


def test_camelize():
    assert camelize('variable_name') == 'variableName'
    assert camelize('variableName') == 'variableName'
    assert camelize('name') == 'name'
    assert camelize('very_long_variable_name') == 'veryLongVariableName'


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
