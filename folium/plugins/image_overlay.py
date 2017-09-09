# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import Element, Figure

from folium.map import Layer
from folium.utilities import image_to_url, mercator_transform

from jinja2 import Template


class ImageOverlay(Layer):
    """
    Used to load and display a single image over specific bounds of
    the map, implements ILayer interface.

    Parameters
    ----------
    image: string, file or array-like object
        The data you want to draw on the map.
        * If string, it will be written directly in the output file.
        * If file, it's content will be converted as embedded in the output file.
        * If array-like, it will be converted to PNG base64 string and embedded in the output.
    bounds: list
        Image bounds on the map in the form [[lat_min, lon_min],
        [lat_max, lon_max]]
    opacity: float, default Leaflet's default (1.0)
    alt: string, default Leaflet's default ('')
    origin: ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or
        lower left corner of the axes.
    colormap: callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4,
        with values between 0 and 1.
        Hint: you can use colormaps from `matplotlib.cm`.
    mercator_project: bool, default False.
        Used only for array-like image.  Transforms the data to
        project (longitude, latitude) coordinates to the
        Mercator projection.
        Beware that this will only work if `image` is an array-like
        object.
    pixelated: bool, default True
        Sharp sharp/crips (True) or aliased corners (False).

    See http://leafletjs.com/reference-1.2.0.html#imageoverlay for more
    options.

    """
    def __init__(self, image, bounds, origin='upper', colormap=None,
                 mercator_project=False, overlay=True, control=True,
                 pixelated=True, name=None, **kwargs):
        super(ImageOverlay, self).__init__(overlay=overlay, control=control, name=name)  # noqa

        options = {
            'opacity': kwargs.pop('opacity', 1.),
            'alt': kwargs.pop('alt', ''),
            'interactive': kwargs.pop('interactive', False),
            'crossOrigin': kwargs.pop('cross_origin', False),
            'errorOverlayUrl': kwargs.pop('error_overlay_url', ''),
            'zIndex': kwargs.pop('zindex', 1),
            'className': kwargs.pop('class_name', ''),
        }
        self._name = 'ImageOverlay'
        self.pixelated = pixelated

        if mercator_project:
            image = mercator_transform(
                image,
                [bounds[0][0],
                 bounds[1][0]],
                origin=origin)

        self.url = image_to_url(image, origin=origin, colormap=colormap)

        self.bounds = json.loads(json.dumps(bounds))
        self.options = json.dumps(options, sort_keys=True, indent=2)
        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.imageOverlay(
                    '{{ this.url }}',
                    {{ this.bounds }},
                    {{ this.options }}
                    ).addTo({{this._parent.get_name()}});
            {% endmacro %}
            """)

    def render(self, **kwargs):
        super(ImageOverlay, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        pixelated = """<style>
        .leaflet-image-layer {
        image-rendering: -webkit-optimize-contrast; /* old android/safari*/
        image-rendering: crisp-edges; /* safari */
        image-rendering: pixelated; /* chrome */
        image-rendering: -moz-crisp-edges; /* firefox */
        image-rendering: -o-crisp-edges; /* opera */
        -ms-interpolation-mode: nearest-neighbor; /* ie */
        }
        </style>"""

        if self.pixelated:
            figure.header.add_child(Element(pixelated), name='leaflet-image-layer')  # noqa

    def _get_self_bounds(self):
        """
        Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]].

        """
        return self.bounds
