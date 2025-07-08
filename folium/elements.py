from functools import wraps

from branca.element import (
    CssLink,
    Element,  # NoQA: F401  needed as a reexport
    Figure,
    JavascriptLink,
    MacroElement,
)

from folium.template import Template
from folium.utilities import JsCode, camelize


def leaflet_method(fn):
    @wraps(fn)
    def inner(self, *args, **kwargs):
        self.add_child(MethodCall(self, fn.__name__, *args, **kwargs))

    return inner


class JSCSSMixin(MacroElement):
    """Render links to external Javascript and CSS resources."""

    default_js: list[tuple[str, str]] = []
    default_css: list[tuple[str, str]] = []

    # Since this is typically used as a mixin, we cannot
    # override the _template member variable here. It would
    # be overwritten by any subclassing class that also has
    # a _template variable.
    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        for name, url in self.default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

        for name, url in self.default_css:
            figure.header.add_child(CssLink(url), name=name)

        super().render(**kwargs)

    def add_css_link(self, name: str, url: str):
        """Add or update css resource link."""
        self._add_link(name, url, self.default_css)

    def add_js_link(self, name: str, url: str):
        """Add or update JS resource link."""
        self._add_link(name, url, self.default_js)

    def _add_link(self, name: str, url: str, default_list: list[tuple[str, str]]):
        """Modify a css or js link.

        If `name` does not exist, the link will be appended
        """

        for i, pair in enumerate(default_list):
            if pair[0] == name:
                default_list[i] = (name, url)
                break
        else:
            default_list.append((name, url))


class EventHandler(MacroElement):
    '''
    Add javascript event handlers.

    Examples
    --------
    >>> import folium
    >>> from folium.utilities import JsCode
    >>>
    >>> m = folium.Map()
    >>>
    >>> geo_json_data = {
    ...     "type": "FeatureCollection",
    ...     "features": [
    ...         {
    ...             "type": "Feature",
    ...             "geometry": {
    ...                 "type": "Polygon",
    ...                 "coordinates": [
    ...                     [
    ...                         [100.0, 0.0],
    ...                         [101.0, 0.0],
    ...                         [101.0, 1.0],
    ...                         [100.0, 1.0],
    ...                         [100.0, 0.0],
    ...                     ]
    ...                 ],
    ...             },
    ...             "properties": {"prop1": {"title": "Somewhere on Sumatra"}},
    ...         }
    ...     ],
    ... }
    >>>
    >>> g = folium.GeoJson(geo_json_data).add_to(m)
    >>>
    >>> highlight = JsCode(
    ...     """
    ...    function highlight(e) {
    ...        e.target.original_color = e.layer.options.color;
    ...        e.target.setStyle({ color: "green" });
    ...    }
    ... """
    ... )
    >>>
    >>> reset = JsCode(
    ...     """
    ...    function reset(e) {
    ...       e.target.setStyle({ color: e.target.original_color });
    ...    }
    ... """
    ... )
    >>>
    >>> g.add_child(EventHandler("mouseover", highlight))
    >>> g.add_child(EventHandler("mouseout", reset))
    '''

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this._parent.get_name()}}.{{ this.method }}(
                {{ this.event|tojson}},
                {{ this.handler.js_code }}
            );
        {% endmacro %}
        """
    )

    def __init__(self, event: str, handler: JsCode, once: bool = False):
        super().__init__()
        self._name = "EventHandler"
        self.event = event
        self.handler = handler
        self.method = "once" if once else "on"


class ElementAddToElement(MacroElement):
    """Abstract class to add an element to another element."""

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this.element_name }}.addTo({{ this.element_parent_name }});
        {% endmacro %}
    """
    )

    def __init__(self, element_name: str, element_parent_name: str):
        super().__init__()
        self.element_name = element_name
        self.element_parent_name = element_parent_name


class IncludeStatement(MacroElement):
    """Generate an include statement on a class."""

    _template = Template(
        """
        {{ this.leaflet_class_name }}.include(
            {{ this.options | tojavascript }}
        )
    """
    )

    def __init__(self, leaflet_class_name: str, **kwargs):
        super().__init__()
        self.leaflet_class_name = leaflet_class_name
        self.options = kwargs

    def render(self, *args, **kwargs):
        return super().render(*args, **kwargs)


class MethodCall(MacroElement):
    """Abstract class to add an element to another element."""

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this.target }}.{{ this.method }}(
                {% for arg in this.args %}
                    {{ arg | tojavascript }},
                {% endfor %}
                {{ this.kwargs | tojavascript }}
            );
        {% endmacro %}
    """
    )

    def __init__(self, target: MacroElement, method: str, *args, **kwargs):
        super().__init__()
        self.target = target.get_name()
        self.method = camelize(method)
        self.args = args
        self.kwargs = kwargs
