"""
Classes for drawing maps.

"""

import warnings
from collections import OrderedDict, defaultdict
from typing import TYPE_CHECKING, DefaultDict, Optional, Sequence, Union, cast

from branca.element import Element, Figure, Html, MacroElement

from folium.elements import ElementAddToElement, EventHandler, IncludeStatement
from folium.template import Template
from folium.utilities import (
    JsCode,
    TypeBounds,
    TypeBoundsReturn,
    TypeJsonValue,
    escape_backticks,
    parse_options,
    remove_empty,
    validate_location,
)


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


if TYPE_CHECKING:
    from folium.features import CustomIcon, DivIcon


class Class(MacroElement):
    """The root class of the leaflet class hierarchy"""

    _includes: DefaultDict[str, dict] = defaultdict(dict)

    @classmethod
    def include(cls, **kwargs):
        cls._includes[cls].update(**kwargs)

    @classproperty
    def includes(cls):
        return cls._includes[cls]

    @property
    def leaflet_class_name(self):
        # TODO: I did not check all Folium classes to see if
        # this holds up. This breaks at least for CustomIcon.
        return f"L.{self._name}"

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."
        if self.includes:
            stmt = IncludeStatement(self.leaflet_class_name, **self.includes)
            # A bit weird. I tried adding IncludeStatement directly to both
            # figure and script, but failed. So we render this ourself.
            figure.script.add_child(
                Element(stmt._template.render(this=stmt, kwargs=self.includes)),
                # make sure each class include gets rendered only once
                name=self._name + "_includes",
                # make sure this renders before the element itself
                index=-1,
            )
        super().render(**kwargs)


class Evented(Class):
    """The base class for Layer and Map

    Adds the `on` and `once` methods for event handling capabilities.

    See https://leafletjs.com/reference.html#evented for
    more in depth documentation. Please note that we have
    only added the `on(<Object> eventMap)` variant of this
    method using python keyword arguments.
    """

    def on(self, **event_map: JsCode):
        self._add(once=False, **event_map)

    def once(self, **event_map: JsCode):
        self._add(once=True, **event_map)

    def _add(self, once: bool, **event_map: JsCode):
        for event_type, handler in event_map.items():
            self.add_child(EventHandler(event_type, handler, once))


class Layer(Evented):
    """An abstract class for everything that is a Layer on the map.
    It will be used to define whether an object will be included in
    LayerControls.

    Parameters
    ----------
    name : string, default None
        The name of the Layer, as it will appear in LayerControls
    overlay : bool, default False
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        overlay: bool = False,
        control: bool = True,
        show: bool = True,
    ):
        super().__init__()
        self.layer_name = name if name is not None else self.get_name()
        self.overlay = overlay
        self.control = control
        self.show = show

    def render(self, **kwargs):
        if self.show:
            self.add_child(
                ElementAddToElement(
                    element_name=self.get_name(),
                    element_parent_name=self._parent.get_name(),
                ),
                name=self.get_name() + "_add",
            )
        super().render(**kwargs)


class FeatureGroup(Layer):
    """
    Create a FeatureGroup layer ; you can put things in it and handle them
    as a single layer.  For example, you can add a LayerControl to
    tick/untick the whole group.

    Parameters
    ----------
    name : str, default None
        The name of the featureGroup layer.
        It will be displayed in the LayerControl.
        If None get_name() will be called to get the technical (ugly) name.
    overlay : bool, default True
        Whether your layer will be an overlay (ticked with a check box in
        LayerControls) or a base layer (ticked with a radio button).
    control: bool, default True
        Whether the layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening.
    **kwargs
        Additional (possibly inherited) options. See
        https://leafletjs.com/reference.html#featuregroup

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.featureGroup(
                {{ this.options|tojavascript }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        name: Optional[str] = None,
        overlay: bool = True,
        control: bool = True,
        show: bool = True,
        **kwargs: TypeJsonValue,
    ):
        super().__init__(name=name, overlay=overlay, control=control, show=show)
        self._name = "FeatureGroup"
        self.tile_name = name if name is not None else self.get_name()
        self.options = remove_empty(**kwargs)


class LayerControl(MacroElement):
    """
    Creates a LayerControl object to be added on a folium map.

    This object should be added to a Map object. Only Layer children
    of Map are included in the layer control.

    Note
    ----
    The LayerControl should be added last to the map.
    Otherwise, the LayerControl and/or the controlled layers may not appear.

    Parameters
    ----------
    position : str
          The position of the control (one of the map corners), can be
          'topleft', 'topright', 'bottomleft' or 'bottomright'
          default: 'topright'
    collapsed : bool, default True
          If true the control will be collapsed into an icon and expanded on
          mouse hover or touch.
    autoZIndex : bool, default True
          If true the control assigns zIndexes in increasing order to all of
          its layers so that the order is preserved when switching them on/off.
    draggable: bool, default False
          By default the layer control has a fixed position. Set this argument
          to True to allow dragging the control around.
    **kwargs
        Additional (possibly inherited) options. See
        https://leafletjs.com/reference.html#control-layers

    """

    _template = Template(
        """
        {% macro script(this,kwargs) %}
            var {{ this.get_name() }}_layers = {
                base_layers : {
                    {%- for key, val in this.base_layers.items() %}
                    {{ key|tojson }} : {{val}},
                    {%- endfor %}
                },
                overlays :  {
                    {%- for key, val in this.overlays.items() %}
                    {{ key|tojson }} : {{val}},
                    {%- endfor %}
                },
            };
            let {{ this.get_name() }} = L.control.layers(
                {{ this.get_name() }}_layers.base_layers,
                {{ this.get_name() }}_layers.overlays,
                {{ this.options|tojavascript }}
            ).addTo({{this._parent.get_name()}});

            {%- if this.draggable %}
            new L.Draggable({{ this.get_name() }}.getContainer()).enable();
            {%- endif %}

        {% endmacro %}
        """
    )

    def __init__(
        self,
        position: str = "topright",
        collapsed: bool = True,
        autoZIndex: bool = True,
        draggable: bool = False,
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "LayerControl"
        self.options = remove_empty(
            position=position, collapsed=collapsed, autoZIndex=autoZIndex, **kwargs
        )
        self.draggable = draggable
        self.base_layers: OrderedDict[str, str] = OrderedDict()
        self.overlays: OrderedDict[str, str] = OrderedDict()

    def reset(self) -> None:
        self.base_layers = OrderedDict()
        self.overlays = OrderedDict()

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        self.reset()
        for item in self._parent._children.values():
            if not isinstance(item, Layer) or not item.control:
                continue
            key = item.layer_name
            if not item.overlay:
                self.base_layers[key] = item.get_name()
            else:
                self.overlays[key] = item.get_name()
        super().render()


class Icon(MacroElement):
    """
    Creates an Icon object that will be rendered
    using Leaflet.awesome-markers.

    Parameters
    ----------
    color : str, default 'blue'
        The color of the marker. You can use:

            ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
             'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
             'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen',
             'gray', 'black', 'lightgray']

    icon_color : str, default 'white'
        The color of the drawing on the marker. You can use colors above,
        or an html color code.
    icon : str, default 'info-sign'
        The name of the marker sign.
        See Font-Awesome website to choose yours.
        Warning : depending on the icon you choose you may need to adapt
        the `prefix` as well.
    angle : int, default 0
        The icon will be rotated by this amount of degrees.
    prefix : str, default 'glyphicon'
        The prefix states the source of the icon. 'fa' for font-awesome or
        'glyphicon' for bootstrap 3.

    https://github.com/lvoogdt/Leaflet.awesome-markers

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.AwesomeMarkers.icon(
                {{ this.options|tojavascript }}
            );
        {% endmacro %}
        """
    )
    color_options = {
        "red",
        "darkred",
        "lightred",
        "orange",
        "beige",
        "green",
        "darkgreen",
        "lightgreen",
        "blue",
        "darkblue",
        "cadetblue",
        "lightblue",
        "purple",
        "darkpurple",
        "pink",
        "white",
        "gray",
        "lightgray",
        "black",
    }

    def __init__(
        self,
        color: str = "blue",
        icon_color: str = "white",
        icon: str = "info-sign",
        angle: int = 0,
        prefix: str = "glyphicon",
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "Icon"
        if color not in self.color_options:
            warnings.warn(
                f"color argument of Icon should be one of: {self.color_options}.",
                stacklevel=2,
            )
        self.options = remove_empty(
            marker_color=color,
            icon_color=icon_color,
            icon=icon,
            prefix=prefix,
            extra_classes=f"fa-rotate-{angle}",
            **kwargs,
        )


class Marker(MacroElement):
    """
    Create a simple stock Leaflet marker on the map, with optional
    popup text or Vincent visualization.

    Parameters
    ----------
    location: tuple or list
        Latitude and Longitude of Marker (Northing, Easting)
    popup: string or folium.Popup, default None
        Label for the Marker; either an escaped HTML string to initialize
        folium.Popup or a folium.Popup instance.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    icon: Icon, CustomIcon or DivIcon, optional
        the Icon plugin to use to render the marker.
    draggable: bool, default False
        Set to True to be able to drag the marker around the map.

    Returns
    -------
    Marker names and HTML in obj.template_vars

    Examples
    --------
    >>> Marker(location=[45.5, -122.3], popup="Portland, OR")
    >>> Marker(location=[45.5, -122.3], popup=Popup("Portland, OR"))
    # If the popup label has characters that need to be escaped in HTML
    >>> Marker(
    ...     location=[45.5, -122.3],
    ...     popup=Popup("Mom & Pop Arrow Shop >>", parse_html=True),
    ... )
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.marker(
                {{ this.location|tojson }},
                {{ this.options|tojavascript }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """
    )

    class SetIcon(MacroElement):
        """Set the icon of a marker after both are created."""

        _template = Template(
            """
            {% macro script(this, kwargs) %}
                {{ this.marker.get_name() }}.setIcon({{ this.icon.get_name() }});
            {% endmacro %}
        """
        )

        def __init__(
            self, marker: "Marker", icon: Union[Icon, "CustomIcon", "DivIcon"]
        ):
            super().__init__()
            self._name = "SetIcon"
            self.marker = marker
            self.icon = icon

    def __init__(
        self,
        location: Optional[Sequence[float]] = None,
        popup: Union["Popup", str, None] = None,
        tooltip: Union["Tooltip", str, None] = None,
        icon: Optional[Union[Icon, "CustomIcon", "DivIcon"]] = None,
        draggable: bool = False,
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "Marker"
        self.location = validate_location(location) if location is not None else None
        self.options = remove_empty(
            draggable=draggable or None, autoPan=draggable or None, **kwargs
        )
        # this attribute is not used by Marker, but by GeoJson
        self.icon = None
        if icon is not None:
            self.set_icon(icon)
        if popup is not None:
            self.add_child(popup if isinstance(popup, Popup) else Popup(str(popup)))
        if tooltip is not None:
            self.add_child(
                tooltip if isinstance(tooltip, Tooltip) else Tooltip(str(tooltip))
            )

    def _get_self_bounds(self) -> TypeBoundsReturn:
        """Computes the bounds of the object itself.

        Because a marker has only single coordinates, we repeat them.
        """
        assert self.location is not None
        return cast(TypeBoundsReturn, [self.location, self.location])

    def render(self):
        if self.location is None:
            raise ValueError(
                f"{self._name} location must be assigned when added directly to map."
            )
        if self.icon:
            self.add_child(self.SetIcon(marker=self, icon=self.icon))
        super().render()

    def set_icon(self, icon):
        """Set the icon for this Marker"""
        super().add_child(icon)
        self.icon = icon

    def add_child(self, child, name=None, index=None):
        import folium.features as features

        if isinstance(child, (Icon, features.CustomIcon, features.DivIcon)):
            self.set_icon(child)
        else:
            super().add_child(child, name, index)
        return self


class Popup(MacroElement):
    """Create a Popup instance that can be linked to a Layer.

    Parameters
    ----------
    html: string or Element
        Content of the Popup.
    parse_html: bool, default False
        True if the popup is a template that needs to the rendered first.
    max_width: int for pixels or text for percentages, default '100%'
        The maximal width of the popup.
    show: bool, default False
        True renders the popup open on page load.
    sticky: bool, default False
        True prevents map and other popup clicks from closing.
    lazy: bool, default False
        True only loads the Popup content when clicking on the Marker.
    """

    _template = Template(
        """
        var {{this.get_name()}} = L.popup({{ this.options|tojavascript }});

        {% for name, element in this.html._children.items() %}
            {% if this.lazy %}
                {{ this._parent.get_name() }}.once('click', function() {
                    {{ this.get_name() }}.setContent($(`{{ element.render(**kwargs).replace('\\n',' ') }}`)[0]);
                });
            {% else %}
                var {{ name }} = $(`{{ element.render(**kwargs).replace('\\n',' ') }}`)[0];
                {{ this.get_name() }}.setContent({{ name }});
            {% endif %}
        {% endfor %}

        {{ this._parent.get_name() }}.bindPopup({{ this.get_name() }})
        {% if this.show %}.openPopup(){% endif %};

        {% for name, element in this.script._children.items() %}
            {{element.render()}}
        {% endfor %}
    """
    )  # noqa

    def __init__(
        self,
        html: Union[str, Element, None] = None,
        parse_html: bool = False,
        max_width: Union[str, int] = "100%",
        show: bool = False,
        sticky: bool = False,
        lazy: bool = False,
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "Popup"
        self.header = Element()
        self.html = Element()
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        script = not parse_html

        if isinstance(html, Element):
            self.html.add_child(html)
        elif isinstance(html, str):
            html = escape_backticks(html)
            self.html.add_child(Html(html, script=script))

        self.show = show
        self.lazy = lazy
        self.options = remove_empty(
            max_width=max_width,
            autoClose=False if show or sticky else None,
            closeOnClick=False if sticky else None,
            **kwargs,
        )

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        for name, child in self._children.items():
            child.render(**kwargs)

        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        figure.script.add_child(
            Element(self._template.render(this=self, kwargs=kwargs)),
            name=self.get_name(),
        )


class Tooltip(MacroElement):
    """
    Create a tooltip that shows text when hovering over its parent object.

    Parameters
    ----------
    text: str
        String to display as a tooltip on the object. If the argument is of a
        different type it will be converted to str.
    style: str, default None.
        HTML inline style properties like font and colors. Will be applied to
        a div with the text in it.
    sticky: bool, default True
        Whether the tooltip should follow the mouse.
    **kwargs
        These values will map directly to the Leaflet Options. More info
        available here: https://leafletjs.com/reference.html#tooltip

    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this._parent.get_name() }}.bindTooltip(
                `<div{% if this.style %} style={{ this.style|tojson }}{% endif %}>
                     {{ this.text }}
                 </div>`,
                {{ this.options|tojavascript }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        text: str,
        style: Optional[str] = None,
        sticky: bool = True,
        **kwargs: TypeJsonValue,
    ):
        super().__init__()
        self._name = "Tooltip"

        self.text = str(text)

        kwargs.update({"sticky": sticky})
        self.options = remove_empty(**kwargs)

        if style:
            assert isinstance(
                style, str
            ), "Pass a valid inline HTML style property string to style."
            # noqa outside of type checking.
            self.style = style


class FitBounds(MacroElement):
    """Fit the map to contain a bounding box with the
    maximum zoom level possible.

    Parameters
    ----------
    bounds: list of (latitude, longitude) points
        Bounding box specified as two points [southwest, northeast]
    padding_top_left: (x, y) point, default None
        Padding in the top left corner. Useful if some elements in
        the corner, such as controls, might obscure objects you're zooming
        to.
    padding_bottom_right: (x, y) point, default None
        Padding in the bottom right corner.
    padding: (x, y) point, default None
        Equivalent to setting both top left and bottom right padding to
        the same value.
    max_zoom: int, default None
        Maximum zoom to be used.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            {{ this._parent.get_name() }}.fitBounds(
                {{ this.bounds|tojson }},
                {{ this.options|tojson }}
            );
        {% endmacro %}
        """
    )

    def __init__(
        self,
        bounds: TypeBounds,
        padding_top_left: Optional[Sequence[float]] = None,
        padding_bottom_right: Optional[Sequence[float]] = None,
        padding: Optional[Sequence[float]] = None,
        max_zoom: Optional[int] = None,
    ):
        super().__init__()
        self._name = "FitBounds"
        self.bounds = bounds
        self.options = parse_options(
            max_zoom=max_zoom,
            padding_top_left=padding_top_left,
            padding_bottom_right=padding_bottom_right,
            padding=padding,
        )


class FitOverlays(MacroElement):
    """Fit the bounds of the maps to the enabled overlays.

    Parameters
    ----------
    padding: int, default 0
        Amount of padding in pixels applied in the corners.
    max_zoom: int, optional
        The maximum possible zoom to use when fitting to the bounds.
    fly: bool, default False
        Use a smoother, longer animation.
    fit_on_map_load: bool, default True
        Apply the fit when initially loading the map.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
        function customFlyToBounds() {
            let bounds = L.latLngBounds([]);
            {{ this._parent.get_name() }}.eachLayer(function(layer) {
                if (typeof layer.getBounds === 'function') {
                    bounds.extend(layer.getBounds());
                }
            });
            if (bounds.isValid()) {
                {{ this._parent.get_name() }}.{{ this.method }}(bounds, {{ this.options|tojavascript }});
            }
        }
        {{ this._parent.get_name() }}.on('overlayadd', customFlyToBounds);
        {%- if this.fit_on_map_load %}
        customFlyToBounds();
        {%- endif %}
        {% endmacro %}
    """
    )

    def __init__(
        self,
        padding: int = 0,
        max_zoom: Optional[int] = None,
        fly: bool = False,
        fit_on_map_load: bool = True,
    ):
        super().__init__()
        self._name = "FitOverlays"
        self.method = "flyToBounds" if fly else "fitBounds"
        self.fit_on_map_load = fit_on_map_load
        self.options = remove_empty(padding=(padding, padding), max_zoom=max_zoom)


class CustomPane(MacroElement):
    """
    Creates a custom pane to hold map elements.

    Behavior is as in https://leafletjs.com/examples/map-panes/

    Parameters
    ----------
    name: string
        Name of the custom pane. Other map elements can be added
        to the pane by specifying the 'pane' kwarg when constructing
        them.
    z_index: int or string, default 625
        The z-index that will be associated with the pane, and will
        determine which map elements lie over/under it. The default
        (625) corresponds to between markers and tooltips. Default
        panes and z-indexes can be found at
        https://leafletjs.com/reference.html#map-pane
    pointer_events: bool, default False
        Whether or not layers in the pane should interact with the
        cursor. Setting to False will prevent interfering with
        pointer events associated with lower layers.
    """

    _template = Template(
        """
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = {{ this._parent.get_name() }}.createPane(
                {{ this.name|tojson }});
            {{ this.get_name() }}.style.zIndex = {{ this.z_index|tojson }};
            {% if not this.pointer_events %}
                {{ this.get_name() }}.style.pointerEvents = 'none';
            {% endif %}
        {% endmacro %}
        """
    )

    def __init__(
        self,
        name: str,
        z_index: Union[int, str] = 625,
        pointer_events: bool = False,
    ):
        super().__init__()
        self._name = "Pane"
        self.name = name
        self.z_index = z_index
        self.pointer_events = pointer_events
