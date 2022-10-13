from folium.elements import JSCSSMixin
from folium.vector_layers import PolyLine


class PolyLineOffset(JSCSSMixin, PolyLine):
    """
    Add offset capabilities to the PolyLine class.

    This plugin adds to folium Polylines the ability to be drawn with a
    relative pixel offset, without modifying their actual coordinates. The offset
    value can be either negative or positive, for left- or right-side offset,
    and remains constant across zoom levels.

    See :func:`folium.vector_layers.path_options` for the `Path` options.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, optional
        Display a text when hovering over the object.
    offset: int, default 0
        Relative pixel offset to draw a line parallel to an existent one,
        at a fixed distance.
    **kwargs:
        Polyline options. See their Github page for the
        available parameters.

    See https://github.com/bbecquet/Leaflet.PolylineOffset

    Examples
    --------
    >>> plugins.PolyLineOffset([[58, -28], [53, -23]], color="#f00", opacity=1, offset=-5).add_to(m)
    >>> plugins.PolyLineOffset([[58, -28], [53, -23]], color="#080", opacity=1, offset=10).add_to(m)

    """

    default_js = [
        ('polylineoffset',
         'https://cdn.jsdelivr.net/npm/leaflet-polylineoffset@1.1.1/leaflet.polylineoffset.min.js')
    ]

    def __init__(self, locations, popup=None, tooltip=None, offset=0, **kwargs):
        super(PolyLineOffset, self).__init__(
            locations=locations, popup=popup, tooltip=tooltip, **kwargs
        )
        self._name = "PolyLineOffset"
        # Add PolyLineOffset offset.
        self.options.update({"offset": offset})
