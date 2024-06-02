from folium.elements import JSCSSMixin
from folium.features import Control
from folium.utilities import JsCode


class MousePosition(JSCSSMixin, Control):
    """Add a field that shows the coordinates of the mouse position.

    Uses the Leaflet plugin by Ardhi Lukianto under MIT license.
    https://github.com/ardhi/Leaflet.MousePosition

    Parameters
    ----------
    position : str, default 'bottomright'
        The standard Control position parameter for the widget.
    separator : str, default ' : '
        Character used to separate latitude and longitude values.
    empty_string : str, default 'Unavailable'
       Initial text to display.
    lng_first : bool, default False
        Whether to put the longitude first or not.
        Set as True to display longitude before latitude.
    num_digits : int, default '5'
        Number of decimal places included in the displayed
        longitude and latitude decimal degree values.
    prefix : str, default ''
        A string to be prepended to the coordinates.
    lat_formatter : str, default None
        Custom Javascript function to format the latitude value.
    lng_formatter : str, default None
        Custom Javascript function to format the longitude value.

    Examples
    --------
    >>> fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    >>> MousePosition(
    ...     position="topright",
    ...     separator=" | ",
    ...     prefix="Mouse:",
    ...     lat_formatter=fmtr,
    ...     lng_formatter=fmtr,
    ... )

    """

    def __init__(
        self,
        position="bottomright",
        separator=" : ",
        empty_string="Unavailable",
        lng_first=False,
        num_digits=5,
        prefix="",
        lat_formatter=None,
        lng_formatter=None,
        **kwargs,
    ):
        super().__init__(
            control="MousePosition",
            position=position,
            separator=separator,
            empty_string=empty_string,
            lng_first=lng_first,
            num_digits=num_digits,
            prefix=prefix,
            lat_formatter=JsCode(lat_formatter) if lat_formatter else None,
            lng_formatter=JsCode(lng_formatter) if lng_formatter else None,
            **kwargs,
        )
        self.add_js_link(
            "Control_MousePosition_js",
            "https://cdn.jsdelivr.net/gh/ardhi/Leaflet.MousePosition/src/L.Control.MousePosition.min.js",
        )
        self.add_css_link(
            "Control_MousePosition_css",
            "https://cdn.jsdelivr.net/gh/ardhi/Leaflet.MousePosition/src/L.Control.MousePosition.min.css",
        )
