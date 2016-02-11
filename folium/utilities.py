# -*- coding: utf-8 -*-
"""
Utilities
-------

Utility module for Folium helper functions.

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import math
import zlib
import struct
import json
import base64
from jinja2 import Environment, PackageLoader

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

from folium.six import text_type, binary_type


def get_templates():
    """Get Jinja templates."""
    return Environment(loader=PackageLoader('folium', 'templates'))


def legend_scaler(legend_values, max_labels=10.0):
    """
    Downsamples the number of legend values so that there isn't a collision
    of text on the legend colorbar (within reason). The colorbar seems to
    support ~10 entries as a maximum.

    """
    if len(legend_values) < max_labels:
        legend_ticks = legend_values
    else:
        spacer = int(math.ceil(len(legend_values)/max_labels))
        legend_ticks = []
        for i in legend_values[::spacer]:
            legend_ticks += [i]
            legend_ticks += ['']*(spacer-1)
    return legend_ticks


def linear_gradient(hexList, nColors):
    """
    Given a list of hexcode values, will return a list of length
    nColors where the colors are linearly interpolated between the
    (r, g, b) tuples that are given.

    Examples
    --------
    >>> linear_gradient([(0, 0, 0), (255, 0, 0), (255, 255, 0)], 100)

    """
    def _scale(start, finish, length, i):
        """
        Return the value correct value of a number that is in between start
        and finish, for use in a loop of length *length*.

        """
        base = 16

        fraction = float(i) / (length - 1)
        raynge = int(finish, base) - int(start, base)
        thex = hex(int(int(start, base) + fraction * raynge)).split('x')[-1]
        if len(thex) != 2:
            thex = '0' + thex
        return thex

    allColors = []
    # Separate (R, G, B) pairs.
    for start, end in zip(hexList[:-1], hexList[1:]):
        # Linearly intepolate between pair of hex ###### values and
        # add to list.
        nInterpolate = 765
        for index in range(nInterpolate):
            r = _scale(start[1:3], end[1:3], nInterpolate, index)
            g = _scale(start[3:5], end[3:5], nInterpolate, index)
            b = _scale(start[5:7], end[5:7], nInterpolate, index)
            allColors.append(''.join(['#', r, g, b]))

    # Pick only nColors colors from the total list.
    result = []
    for counter in range(nColors):
        fraction = float(counter) / (nColors - 1)
        index = int(fraction * (len(allColors) - 1))
        result.append(allColors[index])
    return result


def color_brewer(color_code, n=6):
    """
    Generate a colorbrewer color scheme of length 'len', type 'scheme.
    Live examples can be seen at http://colorbrewer2.org/

    """
    maximum_n = 253

    scheme_info = {'BuGn': 'Sequential',
                   'BuPu': 'Sequential',
                   'GnBu': 'Sequential',
                   'OrRd': 'Sequential',
                   'PuBu': 'Sequential',
                   'PuBuGn': 'Sequential',
                   'PuRd': 'Sequential',
                   'RdPu': 'Sequential',
                   'YlGn': 'Sequential',
                   'YlGnBu': 'Sequential',
                   'YlOrBr': 'Sequential',
                   'YlOrRd': 'Sequential',
                   'BrBg': 'Diverging',
                   'PiYG': 'Diverging',
                   'PRGn': 'Diverging',
                   'PuOr': 'Diverging',
                   'RdBu': 'Diverging',
                   'RdGy': 'Diverging',
                   'RdYlBu': 'Diverging',
                   'RdYlGn': 'Diverging',
                   'Spectral': 'Diverging',
                   'Accent': 'Qualitative',
                   'Dark2': 'Qualitative',
                   'Paired': 'Qualitative',
                   'Pastel1': 'Qualitative',
                   'Pastel2': 'Qualitative',
                   'Set1': 'Qualitative',
                   'Set2': 'Qualitative',
                   'Set3': 'Qualitative',
                   }

    schemes = {'BuGn': ['#EDF8FB', '#CCECE6', '#CCECE6',
                        '#66C2A4', '#41AE76', '#238B45', '#005824'],
               'BuPu': ['#EDF8FB', '#BFD3E6', '#9EBCDA',
                        '#8C96C6', '#8C6BB1', '#88419D', '#6E016B'],
               'GnBu': ['#F0F9E8', '#CCEBC5', '#A8DDB5',
                        '#7BCCC4', '#4EB3D3', '#2B8CBE', '#08589E'],
               'OrRd': ['#FEF0D9', '#FDD49E', '#FDBB84',
                        '#FC8D59', '#EF6548', '#D7301F', '#990000'],
               'PuBu': ['#F1EEF6', '#D0D1E6', '#A6BDDB',
                        '#74A9CF', '#3690C0', '#0570B0', '#034E7B'],
               'PuBuGn': ['#F6EFF7', '#D0D1E6', '#A6BDDB',
                          '#67A9CF', '#3690C0', '#02818A', '#016450'],
               'PuRd': ['#F1EEF6', '#D4B9DA', '#C994C7',
                        '#DF65B0', '#E7298A', '#CE1256', '#91003F'],
               'RdPu': ['#FEEBE2', '#FCC5C0', '#FA9FB5',
                        '#F768A1', '#DD3497', '#AE017E', '#7A0177'],
               'YlGn': ['#FFFFCC', '#D9F0A3', '#ADDD8E',
                        '#78C679', '#41AB5D', '#238443', '#005A32'],
               'YlGnBu': ['#FFFFCC', '#C7E9B4', '#7FCDBB',
                          '#41B6C4', '#1D91C0', '#225EA8', '#0C2C84'],
               'YlOrBr': ['#FFFFD4', '#FEE391', '#FEC44F',
                          '#FE9929', '#EC7014', '#CC4C02', '#8C2D04'],
               'YlOrRd': ['#FFFFB2', '#FED976', '#FEB24C',
                          '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026'],
               'BrBg': ['#8c510a', '#d8b365', '#f6e8c3',
                        '#c7eae5', '#5ab4ac', '#01665e'],
               'PiYG': ['#c51b7d', '#e9a3c9', '#fde0ef',
                        '#e6f5d0', '#a1d76a', '#4d9221'],
               'PRGn': ['#762a83', '#af8dc3', '#e7d4e8',
                        '#d9f0d3', '#7fbf7b', '#1b7837'],
               'PuOr': ['#b35806', '#f1a340', '#fee0b6',
                        '#d8daeb', '#998ec3', '#542788'],
               'RdBu': ['#b2182b', '#ef8a62', '#fddbc7',
                        '#d1e5f0', '#67a9cf', '#2166ac'],
               'RdGy': ['#b2182b', '#ef8a62', '#fddbc7',
                        '#e0e0e0', '#999999', '#4d4d4d'],
               'RdYlBu': ['#d73027', '#fc8d59', '#fee090',
                          '#e0f3f8', '#91bfdb', '#4575b4'],
               'RdYlGn': ['#d73027', '#fc8d59', '#fee08b',
                          '#d9ef8b', '#91cf60', '#1a9850'],
               'Spectral': ['#d53e4f', '#fc8d59', '#fee08b',
                            '#e6f598', '#99d594', '#3288bd'],
               'Accent': ['#7fc97f', '#beaed4', '#fdc086',
                          '#ffff99', '#386cb0', '#f0027f'],
               'Dark2': ['#1b9e77', '#d95f02', '#7570b3',
                         '#e7298a', '#66a61e', '#e6ab02'],
               'Paired': ['#a6cee3', '#1f78b4', '#b2df8a',
                          '#33a02c', '#fb9a99', '#e31a1c'],
               'Pastel1': ['#fbb4ae', '#b3cde3', '#ccebc5',
                           '#decbe4', '#fed9a6', '#ffffcc'],
               'Pastel2': ['#b3e2cd', '#fdcdac', '#cbd5e8',
                           '#f4cae4', '#e6f5c9', '#fff2ae'],
               'Set1': ['#e41a1c', '#377eb8', '#4daf4a',
                        '#984ea3', '#ff7f00', '#ffff33'],
               'Set2': ['#66c2a5', '#fc8d62', '#8da0cb',
                        '#e78ac3', '#a6d854', '#ffd92f'],
               'Set3': ['#8dd3c7', '#ffffb3', '#bebada',
                        '#fb8072', '#80b1d3', '#fdb462'],
               }

    # Raise an error if the n requested is greater than the maximum.
    if n > maximum_n:
        raise ValueError("The maximum number of colors in a"
                         " ColorBrewer sequential color series is 253")

    # Only if n is greater than six do we interpolate values.
    if n > 6:
        if color_code not in schemes:
            color_scheme = None
        else:
            # Check to make sure that it is not a qualitative scheme.
            if scheme_info[color_code] == 'Qualitative':
                raise ValueError("Expanded color support is not available"
                                 " for Qualitative schemes, restrict"
                                 " number of colors to 6")
            else:
                color_scheme = linear_gradient(schemes.get(color_code), n)
    else:
        color_scheme = schemes.get(color_code, None)
    return color_scheme


def split_six(series=None):
    """
    Given a Pandas Series, get a domain of values from zero to the 90% quantile
    rounded to the nearest order-of-magnitude integer. For example, 2100 is
    rounded to 2000, 2790 to 3000.

    Parameters
    ----------
    series: Pandas series, default None

    Returns
    -------
    list

    """
    if pd is None:
        raise ImportError("The Pandas package is required"
                          " for this functionality")
    if np is None:
        raise ImportError("The NumPy package is required"
                          " for this functionality")

    def base(x):
        if x > 0:
            base = pow(10, math.floor(math.log10(x)))
            return round(x/base)*base
        else:
            return 0

    quants = [0, 50, 75, 85, 90]
    # Some weirdness in series quantiles a la 0.13.
    arr = series.values
    return [base(np.percentile(arr, x)) for x in quants]


def image_to_url(image, colormap=None, origin='upper'):
    """Infers the type of an image argument and transforms it into a URL.

    Parameters
    ----------
    image: string, file or array-like object
        * If string, it will be written directly in the output file.
        * If file, it's content will be converted as embedded in the
          output file.
        * If array-like, it will be converted to PNG base64 string and
          embedded in the output.
    origin : ['upper' | 'lower'], optional, default 'upper'
        Place the [0, 0] index of the array in the upper left or
        lower left corner of the axes.
    colormap : callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4, with values between
        0. and 1.  Hint : you can use colormaps from `matplotlib.cm`.
    """
    if hasattr(image, 'read'):
        # We got an image file.
        if hasattr(image, 'name'):
            # We try to get the image format from the file name.
            fileformat = image.name.lower().split('.')[-1]
        else:
            fileformat = 'png'
        url = "data:image/{};base64,{}".format(
            fileformat, base64.b64encode(image.read()).decode('utf-8'))
    elif (not (isinstance(image, text_type) or
               isinstance(image, binary_type))) and hasattr(image, '__iter__'):
        # We got an array-like object.
        png = write_png(image, origin=origin, colormap=colormap)
        url = "data:image/png;base64," + base64.b64encode(png).decode('utf-8')
    else:
        # We got an URL.
        url = json.loads(json.dumps(image))

    return url.replace('\n', ' ')


def write_png(data, origin='upper', colormap=None):
    """
    Transform an array of data into a PNG string.
    This can be written to disk using binary I/O, or encoded using base64
    for an inline PNG like this:

    >>> png_str = write_png(array)
    >>> "data:image/png;base64,"+png_str.encode('base64')

    Inspired from
    http://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image

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
        raise ImportError("The NumPy package is required"
                          " for this functionality")

    if colormap is None:
        def colormap(x):
            return (x, x, x, 1)

    array = np.atleast_3d(data)
    height, width, nblayers = array.shape

    if nblayers not in [1, 3, 4]:
            raise ValueError("Data must be NxM (mono), "
                             "NxMx3 (RGB), or NxMx4 (RGBA)")
    assert array.shape == (height, width, nblayers)

    if nblayers == 1:
        array = np.array(list(map(colormap, array.ravel())))
        nblayers = array.shape[1]
        if nblayers not in [3, 4]:
            raise ValueError("colormap must provide colors of"
                             "length 3 (RGB) or 4 (RGBA)")
        array = array.reshape((height, width, nblayers))
    assert array.shape == (height, width, nblayers)

    if nblayers == 3:
        array = np.concatenate((array, np.ones((height, width, 1))), axis=2)
        nblayers = 4
    assert array.shape == (height, width, nblayers)
    assert nblayers == 4

    # Normalize to uint8 if it isn't already.
    if array.dtype != 'uint8':
        array = array * 255./array.max(axis=(0, 1)).reshape((1, 1, 4))
        array = array.astype('uint8')

    # Eventually flip the image.
    if origin == 'lower':
        array = array[::-1, :, :]

    # Transform the array to bytes.
    raw_data = b''.join([b'\x00' + array[i, :, :].tobytes()
                         for i in range(height)])

    def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return (struct.pack("!I", len(data)) +
                    chunk_head +
                    struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])


def _camelify(out):
    return (''.join(["_" + x.lower() if i < len(out)-1 and x.isupper() and out[i+1].islower()  # noqa
         else x.lower() + "_" if i < len(out)-1 and x.islower() and out[i+1].isupper()  # noqa
         else x.lower() for i, x in enumerate(list(out))])).lstrip('_').replace('__', '_')  # noqa


def _parse_size(value):
    try:
        if isinstance(value, int) or isinstance(value, float):
            value_type = 'px'
            value = float(value)
            assert value > 0
        else:
            value_type = '%'
            value = float(value.strip('%'))
            assert 0 <= value <= 100
    except:
        msg = "Cannot parse value {!r} as {!r}".format
        raise ValueError(msg(value, value_type))
    return value, value_type


def _locations_mirror(x):
    """Mirrors the points in a list-of-list-of-...-of-list-of-points.
    For example:
    >>> _locations_mirror([[[1, 2], [3, 4]], [5, 6], [7, 8]])
    [[[2, 1], [4, 3]], [6, 5], [8, 7]]

    """
    if hasattr(x, '__iter__'):
        if hasattr(x[0], '__iter__'):
            return list(map(_locations_mirror, x))
        else:
            return list(x[::-1])
    else:
        return x


def _locations_tolist(x):
    """Transforms recursively a list of iterables into a list of list.
    """
    if hasattr(x, '__iter__'):
        return list(map(_locations_tolist, x))
    else:
        return x


def none_min(x, y):
    if x is None:
        return y
    elif y is None:
        return x
    else:
        return min(x, y)


def none_max(x, y):
    if x is None:
        return y
    elif y is None:
        return x
    else:
        return max(x, y)


def iter_points(x):
    """Iterates over a list representing a feature, and returns a list of points,
    whatever the shape of the array (Point, MultiPolyline, etc).
    """
    if isinstance(x, (list, tuple)):
        if len(x):
            if isinstance(x[0], (list, tuple)):
                out = []
                for y in x:
                    out += iter_points(y)
                return out
            else:
                return [x]
        else:
            return []
    else:
        raise ValueError('List/tuple type expected. Got {!r}.'.format(x))
