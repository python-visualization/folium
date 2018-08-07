from __future__ import (absolute_import, division, print_function)

from folium.utilities import camelize


def test_camelize():
    assert camelize('variable_name') == 'variableName'
    assert camelize('variableName') == 'variableName'
    assert camelize('name') == 'name'
    assert camelize('very_long_variable_name') == 'veryLongVariableName'
