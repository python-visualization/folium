import numpy as np
import pandas as pd
import pytest

from folium import Map, FeatureGroup, Marker, Popup
from folium.utilities import (
    validate_location,
    validate_locations,
    if_pandas_df_convert_to_numpy,
    camelize,
    deep_copy,
    get_obj_in_upper_tree,
    parse_options,
    _is_url,
)


@pytest.mark.parametrize('location', [
    (5, 3),
    [5., 3.],
    np.array([5, 3]),
    np.array([[5, 3]]),
    pd.Series([5, 3]),
    pd.DataFrame([5, 3]),
    pd.DataFrame([[5, 3]]),
    ('5.0', '3.0'),
    ('5', '3'),
])
def test_validate_location(location):
    outcome = validate_location(location)
    assert outcome == [5., 3.]


@pytest.mark.parametrize('location', [
    None,
    [None, None],
    (),
    [0],
    ['hi'],
    'hi',
    ('lat', 'lon'),
    Marker,
    (Marker, Marker),
    (3., np.nan),
    {3., 5.},
    {'lat': 5., 'lon': 3.},
    range(4),
    [0, 1, 2],
    [(0, ), (1, )],
])
def test_validate_location_exceptions(location):
    """Test input that should raise an exception."""
    with pytest.raises((TypeError, ValueError)):
        validate_location(location)


@pytest.mark.parametrize('locations', [
    [(0, 5), (1, 6), (2, 7)],
    [[0, 5], [1, 6], [2, 7]],
    np.array([[0, 5], [1, 6], [2, 7]]),
    pd.DataFrame([[0, 5], [1, 6], [2, 7]]),
])
def test_validate_locations(locations):
    outcome = validate_locations(locations)
    assert outcome == [[0., 5.], [1., 6.], [2., 7.]]


@pytest.mark.parametrize('locations', [
    [[(0, 5), (1, 6), (2, 7)], [(3, 8), (4, 9)]],
])
def test_validate_locations_multi(locations):
    outcome = validate_locations(locations)
    assert outcome == [[[0, 5], [1, 6], [2, 7]], [[3, 8], [4, 9]]]


@pytest.mark.parametrize('locations', [
    None,
    [None, None],
    (),
    [0],
    ['hi'],
    'hi',
    ('lat', 'lon'),
    Marker,
    (Marker, Marker),
    (3., np.nan),
    {3., 5.},
    {'lat': 5., 'lon': 3.},
    range(4),
    [0, 1, 2],
    [(0, ), (1, )],
])
def test_validate_locations_exceptions(locations):
    """Test input that should raise an exception."""
    with pytest.raises((TypeError, ValueError)):
        validate_locations(locations)


def test_if_pandas_df_convert_to_numpy():
    data = [[0, 5, 'red'], [1, 6, 'blue'], [2, 7, 'something']]
    df = pd.DataFrame(data, columns=['lat', 'lng', 'color'])
    res = if_pandas_df_convert_to_numpy(df)
    assert isinstance(res, np.ndarray)
    expected = np.array(data)
    assert all([[all([i == j]) for i, j in zip(row1, row2)]
                for row1, row2 in zip(res, expected)])
    # Also check if it ignores things that are not Pandas DataFrame:
    assert if_pandas_df_convert_to_numpy(data) is data
    assert if_pandas_df_convert_to_numpy(expected) is expected


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


def test_parse_options():
    assert parse_options(thing=42) == {'thing': 42}
    assert parse_options(thing=None) == {}
    assert parse_options(long_thing=42) == {'longThing': 42}
    assert parse_options(thing=42, lst=[1, 2]) == {'thing': 42, 'lst': [1, 2]}


@pytest.mark.parametrize('url', [
    "https://example.com/img.png",
    "http://example.com/img.png",
    "ftp://example.com/img.png",
    "file:///t.jpg",
    "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
])
def test_is_url(url):
    assert _is_url(url) is True
