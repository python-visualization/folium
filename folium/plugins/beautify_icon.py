from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.utilities import parse_options


class BeautifyIcon(JSCSSMixin, MacroElement):
    """
    Create a BeautifyIcon that can be added to a Marker

    Parameters
    ----------
    icon: string, default None
        the Font-Awesome icon name to use to render the marker.
    icon_shape: string, default None
        the icon shape
    border_width: integer, default 3
        the border width of the icon
    border_color: string with hexadecimal RGB, default '#000'
        the border color of the icon
    text_color: string with hexadecimal RGB, default '#000'
        the text color of the icon
    background_color: string with hexadecimal RGB, default '#FFF'
        the background color of the icon
    inner_icon_style: string with css styles for the icon, default ''
        the css styles of the icon
    spin: boolean, default False
        allow the icon to be spinning.
    number: integer, default None
        the number of the icon.

    Examples
    --------
    Plugin Website: https://github.com/masajid390/BeautifyMarker
    >>> BeautifyIcon(
    ...     text_color="#000", border_color="transparent", background_color="#FFF"
    ... ).add_to(marker)
    >>> number_icon = BeautifyIcon(
    ...     text_color="#000",
    ...     border_color="transparent",
    ...     background_color="#FFF",
    ...     number=10,
    ...     inner_icon_style="font-size:12px;padding-top:-5px;",
    ... )
    >>> Marker(
    ...     location=[45.5, -122.3],
    ...     popup=folium.Popup("Portland, OR"),
    ...     icon=number_icon,
    ... )
    >>> BeautifyIcon(icon="arrow-down", icon_shape="marker").add_to(marker)

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = new L.BeautifyIcon.icon(
                {{ this.options|tojson }}
            )
            {{ this._parent.get_name() }}.setIcon({{ this.get_name() }});
        {% endmacro %}
        """
    )
    ICON_SHAPE_TYPES = [
        "circle",
        "circle-dot",
        "doughnut",
        "rectangle-dot",
        "marker",
        None,
    ]

    default_js = [
        (
            "beautify_icon_js",
            "https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.js",
        )
    ]
    default_css = [
        (
            "beautify_icon_css",
            "https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.css",
        )
    ]

    def __init__(
        self,
        icon=None,
        icon_shape=None,
        border_width=3,
        border_color="#000",
        text_color="#000",
        background_color="#FFF",
        inner_icon_style="",
        spin=False,
        number=None,
        **kwargs,
    ):
        super().__init__()
        self._name = "BeautifyIcon"

        self.options = parse_options(
            icon=icon,
            icon_shape=icon_shape,
            border_width=border_width,
            border_color=border_color,
            text_color=text_color,
            background_color=background_color,
            inner_icon_style=inner_icon_style,
            spin=spin,
            isAlphaNumericIcon=number is not None,
            text=number,
            **kwargs,
        )
