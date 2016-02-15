# -*- coding: utf-8 -*-
"""
Image Overlay
-------------

Used to load and display a single image over specific bounds of
the map, implements ILayer interface.

"""
import json
from jinja2 import Template

from branca.utilities import image_to_url

from folium.map import Layer


def mercator_transform(data, lat_bounds, origin='upper', height_out=None):
    """Transforms an image computed in (longitude,latitude) coordinates into
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


class ImageOverlay(Layer):
    def __init__(self, image, bounds, opacity=1., attr=None,
                 origin='upper', colormap=None, mercator_project=False,
                 overlay=True, control=True):
        """
        Used to load and display a single image over specific bounds of
        the map, implements ILayer interface.

        Parameters
        ----------
        image: string, file or array-like object
            The data you want to draw on the map.
            * If string, it will be written directly in the output file.
            * If file, it's content will be converted as embedded in the
              output file.
            * If array-like, it will be converted to PNG base64 string
              and embedded in the output.
        bounds: list
            Image bounds on the map in the form [[lat_min, lon_min],
            [lat_max, lon_max]]
        opacity: float, default Leaflet's default (1.0)
        attr: string, default Leaflet's default ("")
        origin : ['upper' | 'lower'], optional, default 'upper'
            Place the [0,0] index of the array in the upper left or
            lower left corner of the axes.
        colormap : callable, used only for `mono` image.
            Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
            for transforming a mono image into RGB.
            It must output iterables of length 3 or 4,
            with values between 0 and 1.
            Hint : you can use colormaps from `matplotlib.cm`.
        mercator_project : bool, default False.
            Used only for array-like image.  Transforms the data to
            project (longitude, latitude) coordinates to the
            Mercator projection.
            Beware that this will only work if `image` is an array-like
            object.

        """
        super(ImageOverlay, self).__init__(overlay=overlay, control=control)
        self._name = 'ImageOverlay'
        self.overlay = overlay

        if mercator_project:
            image = mercator_transform(image,
                                       [bounds[0][0], bounds[1][0]],
                                       origin=origin)

        self.url = image_to_url(image, origin=origin, colormap=colormap)

        self.bounds = json.loads(json.dumps(bounds))
        options = {
            'opacity': opacity,
            'attribution': attr,
        }
        self.options = json.dumps({key: val for key, val
                                   in options.items() if val},
                                  sort_keys=True)
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.imageOverlay(
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def _get_self_bounds(self):
        """Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]
        """
        return self.bounds
