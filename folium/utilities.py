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


def _parse_path(**kw):
    """Parse Path http://leafletjs.com/reference-1.2.0.html#path options."""
    color = kw.pop('color', '#3388ff')
    return {
        'stroke': kw.pop('stroke', True),
        'color': color,
        'weight': kw.pop('weight', 3),
        'opacity': kw.pop('opacity', 1.0),
        'lineCap': kw.pop('line_cap', 'round'),
        'lineJoin': kw.pop('line_join', 'round'),
        'dashArray': kw.pop('dash_array', None),
        'dashOffset': kw.pop('dash_offset', None),
        'fill': kw.pop('fill', False),
        'fillColor': kw.pop('fill_color', color),
        'fillOpacity': kw.pop('fill_opacity', 0.2),
        'fillRule': kw.pop('fill_rule', 'evenodd'),
        'bubblingMouseEvents': kw.pop('bubbling_mouse_events', True),
    }


def _parse_wms(**kw):
    """Parse tilelayer-wms http://leafletjs.com/reference-1.2.0.html#tilelayer-wms options."""
    return {
        'layers': kw.pop('layers', ''),
        'styles': kw.pop('styles', ''),
        'format': kw.pop('fmt', 'image/jpeg'),
        'transparent': kw.pop('transparent', False),
        'version': kw.pop('version', '1.1.1'),
        'crs': kw.pop('crs', None),
        'uppercase': kw.pop('uppercase', False),
    }
