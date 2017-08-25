from __future__ import (absolute_import, division, print_function)

import math


def _validate_location(location):
    """Validates and formats location values before setting."""
    if _isnan(location):
        raise ValueError('Location values cannot contain NaNs, '
                         'got {!r}'.format(location))
    if type(location) not in [list, tuple]:
        raise TypeError('Expected tuple/list for location, got '
                        '{!r}'.format(location))

    if len(location) != 2:
        raise ValueError('Expected two values for location [lat, lon], '
                         'got {}'.format(len(location)))
    location = _locations_tolist(location)
    return location


def _validate_coordinates(coordinates):
    """Validates multiple coordinates for the various markers in folium."""
    if _isnan(coordinates):
        raise ValueError('Location values cannot contain NaNs, '
                         'got:\n{!r}'.format(coordinates))
    coordinates = _locations_tolist(coordinates)
    return coordinates


def _locations_tolist(x):
    """Transforms recursively a list of iterables into a list of list."""
    if hasattr(x, '__iter__'):
        return list(map(_locations_tolist, x))
    else:
        return x


def _flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in _flatten(i):
                yield j
        else:
            yield i


def _isnan(values):
    """Check if there are NaNs values in the iterable."""
    return any(math.isnan(value) for value in _flatten(values))
