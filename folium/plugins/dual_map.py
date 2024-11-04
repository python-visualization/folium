from branca.element import Figure, MacroElement

from folium.elements import JSCSSMixin
from folium.folium import Map
from folium.map import LayerControl
from folium.template import Template
from folium.utilities import deep_copy


class DualMap(JSCSSMixin, MacroElement):
    """Create two maps in the same window.

    Adding children to this objects adds them to both maps. You can access
    the individual maps with `DualMap.m1` and `DualMap.m2`.

    Uses the Leaflet plugin Sync: https://github.com/jieter/Leaflet.Sync

    Parameters
    ----------
    location: tuple or list, optional
        Latitude and longitude of center point of the maps.
    layout : {'horizontal', 'vertical'}
        Select how the two maps should be positioned. Either horizontal (left
        and right) or vertical (top and bottom).
    **kwargs
        Keyword arguments are passed to the two Map objects.

    Examples
    --------
    >>> # DualMap accepts the same arguments as Map:
    >>> m = DualMap(location=(0, 0), tiles="cartodbpositron", zoom_start=5)
    >>> # Add the same marker to both maps:
    >>> Marker((0, 0)).add_to(m)
    >>> # The individual maps are attributes called `m1` and `m2`:
    >>> Marker((0, 1)).add_to(m.m1)
    >>> LayerControl().add_to(m)
    >>> m.save("map.html")

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this.m1.get_name() }}.sync({{ this.m2.get_name() }});
            {{ this.m2.get_name() }}.sync({{ this.m1.get_name() }});
        {% endmacro %}
    """
    )

    default_js = [
        (
            "Leaflet.Sync",
            "https://cdn.jsdelivr.net/gh/jieter/Leaflet.Sync/L.Map.Sync.min.js",
        )
    ]

    def __init__(self, location=None, layout="horizontal", **kwargs):
        super().__init__()
        for key in ("width", "height", "left", "top", "position"):
            assert key not in kwargs, f"Argument {key} cannot be used with  DualMap."
        if layout not in ("horizontal", "vertical"):
            raise ValueError(
                f"Undefined option for argument `layout`: {layout}. "
                "Use either 'horizontal' or 'vertical'."
            )
        width = "50%" if layout == "horizontal" else "100%"
        height = "100%" if layout == "horizontal" else "50%"
        self.m1 = Map(
            location=location,
            width=width,
            height=height,
            left="0%",
            top="0%",
            position="absolute",
            **kwargs,
        )
        self.m2 = Map(
            location=location,
            width=width,
            height=height,
            left="50%" if layout == "horizontal" else "0%",
            top="0%" if layout == "horizontal" else "50%",
            position="absolute",
            **kwargs,
        )
        figure = Figure()
        figure.add_child(self.m1)
        figure.add_child(self.m2)
        # Important: add self to Figure last.
        figure.add_child(self)
        self.children_for_m2 = []
        self.children_for_m2_copied = []  # list with ids

    def _repr_html_(self, **kwargs):
        """Displays the HTML Map in a Jupyter notebook."""
        if self._parent is None:
            self.add_to(Figure())
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out

    def add_child(self, child, name=None, index=None):
        """Add object `child` to the first map and store it for the second."""
        self.m1.add_child(child, name, index)
        if index is None:
            index = len(self.m2._children)
        self.children_for_m2.append((child, name, index))

    def render(self, **kwargs):
        super().render(**kwargs)

        for child, name, index in self.children_for_m2:
            if child._id in self.children_for_m2_copied:
                # This map has been rendered before, child was copied already.
                continue
            child_copy = deep_copy(child)
            if isinstance(child_copy, LayerControl):
                child_copy.reset()
            self.m2.add_child(child_copy, name, index)
            # m2 has already been rendered, so render the child here:
            child_copy.render()
            self.children_for_m2_copied.append(child._id)

    def fit_bounds(self, *args, **kwargs):
        for m in (self.m1, self.m2):
            m.fit_bounds(*args, **kwargs)

    def keep_in_front(self, *args):
        for m in (self.m1, self.m2):
            m.keep_in_front(*args)
