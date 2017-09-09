from __future__ import (absolute_import, division, print_function)

import base64
import io
import json
import math
import os
import struct
import zlib

from six import binary_type, text_type

try:
    import numpy as np
except ImportError:
    np = None

try:
    from urllib.parse import uses_relative, uses_netloc, uses_params, urlparse
except ImportError:
    from urlparse import uses_relative, uses_netloc, uses_params, urlparse


_VALID_URLS = set(uses_relative + uses_netloc + uses_params)
_VALID_URLS.discard('')


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
    """
    Parse leaflet `Path` options.
    http://leafletjs.com/reference-1.2.0.html#path

    """
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
    """
    Parse leaflet TileLayer.WMS options.
    http://leafletjs.com/reference-1.2.0.html#tilelayer-wms

    """
    return {
        'layers': kw.pop('layers', ''),
        'styles': kw.pop('styles', ''),
        'format': kw.pop('fmt', 'image/jpeg'),
        'transparent': kw.pop('transparent', False),
        'version': kw.pop('version', '1.1.1'),
        'crs': kw.pop('crs', None),
        'uppercase': kw.pop('uppercase', False),
    }


def image_to_url(image, colormap=None, origin='upper'):
    """
    Infers the type of an image argument and transforms it into a URL.

    Parameters
    ----------
    image: string, file or array-like object
        * If string, it will be written directly in the output file.
        * If file, it's content will be converted as embedded in the
          output file.
        * If array-like, it will be converted to PNG base64 string and
          embedded in the output.
    origin: ['upper' | 'lower'], optional, default 'upper'
        Place the [0, 0] index of the array in the upper left or
        lower left corner of the axes.
    colormap: callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4, with values between
        0. and 1.  You can use colormaps from `matplotlib.cm`.

    """
    if isinstance(image, (text_type, binary_type)) and not _is_url(image):
        fileformat = os.path.splitext(image)[-1][1:]
        with io.open(image, 'rb') as f:
            img = f.read()
        b64encoded = base64.b64encode(img).decode('utf-8')
        url = 'data:image/{};base64,{}'.format(fileformat, b64encoded)
    elif 'ndarray' in image.__class__.__name__:
        img = write_png(image, origin=origin, colormap=colormap)
        b64encoded = base64.b64encode(img).decode('utf-8')
        url = 'data:image/png;base64,{}'.format(b64encoded)
    else:
        # Round-trip to ensure a nice formatted json.
        url = json.loads(json.dumps(image))
    return url.replace('\n', ' ')


def _is_url(url):
    """Check to see if `url` has a valid protocol."""
    try:
        return urlparse(url).scheme in _VALID_URLS
    except:
        return False


def write_png(data, origin='upper', colormap=None):
    """
    Transform an array of data into a PNG string.
    This can be written to disk using binary I/O, or encoded using base64
    for an inline PNG like this:

    >>> png_str = write_png(array)
    >>> "data:image/png;base64,"+png_str.encode('base64')

    Inspired from
    https://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image

    Parameters
    ----------
    data: numpy array or equivalent list-like object.
         Must be NxM (mono), NxMx3 (RGB) or NxMx4 (RGBA)

    origin : ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or lower left
        corner of the axes.

    colormap : callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4, with values between
        0. and 1.  Hint: you can use colormaps from `matplotlib.cm`.

    Returns
    -------
    PNG formatted byte string

    """
    if np is None:
        raise ImportError('The NumPy package is required '
                          ' for this functionality')

    if colormap is None:
        def colormap(x):
            return (x, x, x, 1)

    arr = np.atleast_3d(data)
    height, width, nblayers = arr.shape

    if nblayers not in [1, 3, 4]:
            raise ValueError('Data must be NxM (mono), '
                             'NxMx3 (RGB), or NxMx4 (RGBA)')
    assert arr.shape == (height, width, nblayers)

    if nblayers == 1:
        arr = np.array(list(map(colormap, arr.ravel())))
        nblayers = arr.shape[1]
        if nblayers not in [3, 4]:
            raise ValueError('colormap must provide colors of r'
                             'length 3 (RGB) or 4 (RGBA)')
        arr = arr.reshape((height, width, nblayers))
    assert arr.shape == (height, width, nblayers)

    if nblayers == 3:
        arr = np.concatenate((arr, np.ones((height, width, 1))), axis=2)
        nblayers = 4
    assert arr.shape == (height, width, nblayers)
    assert nblayers == 4

    # Normalize to uint8 if it isn't already.
    if arr.dtype != 'uint8':
        with np.errstate(divide='ignore', invalid='ignore'):
            arr = arr * 255./arr.max(axis=(0, 1)).reshape((1, 1, 4))
            arr[~np.isfinite(arr)] = 0
        arr = arr.astype('uint8')

    # Eventually flip the image.
    if origin == 'lower':
        arr = arr[::-1, :, :]

    # Transform the array to bytes.
    raw_data = b''.join([b'\x00' + arr[i, :, :].tobytes()
                         for i in range(height)])

    def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return (struct.pack('!I', len(data)) +
                    chunk_head +
                    struct.pack('!I', 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack('!2I5B', width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])


def mercator_transform(data, lat_bounds, origin='upper', height_out=None):
    """
    Transforms an image computed in (longitude,latitude) coordinates into
    the a Mercator projection image.

    Parameters
    ----------

    data: numpy array or equivalent list-like object.
        Must be NxM (mono), NxMx3 (RGB) or NxMx4 (RGBA)

    lat_bounds : length 2 tuple
        Minimal and maximal value of the latitude of the image.
        Bounds must be between -85.051128779806589 and 85.051128779806589
        otherwise they will be clipped to that values.

    origin : ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or lower left
        corner of the axes.

    height_out : int, default None
        The expected height of the output.
        If None, the height of the input is used.

    See https://en.wikipedia.org/wiki/Web_Mercator for more details.

    """
    import numpy as np

    def mercator(x):
        return np.arcsinh(np.tan(x*np.pi/180.))*180./np.pi

    array = np.atleast_3d(data).copy()
    height, width, nblayers = array.shape

    lat_min = max(lat_bounds[0], -85.051128779806589)
    lat_max = min(lat_bounds[1], 85.051128779806589)
    if height_out is None:
        height_out = height

    # Eventually flip the image
    if origin == 'upper':
        array = array[::-1, :, :]

    lats = (lat_min + np.linspace(0.5/height, 1.-0.5/height, height) *
            (lat_max-lat_min))
    latslats = (mercator(lat_min) +
                np.linspace(0.5/height_out, 1.-0.5/height_out, height_out) *
                (mercator(lat_max)-mercator(lat_min)))

    out = np.zeros((height_out, width, nblayers))
    for i in range(width):
        for j in range(nblayers):
            out[:, i, j] = np.interp(latslats, mercator(lats),  array[:, i, j])

    # Eventually flip the image.
    if origin == 'upper':
        out = out[::-1, :, :]
    return out
