from __future__ import annotations

import re
from collections.abc import Sequence

from folium.elements import JSCSSMixin
from folium.raster_layers import TileLayer

# CSS filter functions supported by Leaflet.TileLayer.ColorFilter, with the unit
# the plugin appends to a bare number and the short names the plugin also
# accepts.
_FILTERS = {
    "blur": ("px", ()),
    "brightness": ("%", ("bright", "bri")),
    "contrast": ("%", ("con",)),
    "grayscale": ("%", ("gray",)),
    "hue-rotate": ("deg", ("hue", "hue-rotation")),
    "invert": ("%", ("inv",)),
    "opacity": ("%", ("op",)),
    "saturate": ("%", ("sat", "saturation")),
    "sepia": ("%", ("sep",)),
}

_ALIASES = {alias: name for name, (_, aliases) in _FILTERS.items() for alias in aliases}

_VALUE = re.compile(r"(?P<number>\d+)(?P<unit>%|deg|px)?")


def _normalize_color_filter(color_filter: str | Sequence[str]) -> list[str]:
    """Validate color filter definitions and return them in canonical form.

    Each filter is written as ``"<name>:<number><unit>"``. The plugin silently
    drops a filter it does not understand, which leaves the map looking as if
    nothing was configured, so the definitions are checked here instead.
    """
    if isinstance(color_filter, str):
        color_filter = [color_filter]
    filters = []
    for item in color_filter:
        if not isinstance(item, str):
            raise ValueError(
                f"Filters must be strings like 'invert:100%', got {item!r}."
            )
        name, _, value = item.partition(":")
        name = _ALIASES.get(name.strip().lower(), name.strip().lower())
        value = value.strip().lower()
        if name not in _FILTERS:
            valid = ", ".join(sorted(_FILTERS))
            aliases = ", ".join(sorted(_ALIASES))
            raise ValueError(
                f"Unknown color filter {name!r}. Valid filters are: {valid}. "
                f"Short names: {aliases}."
            )
        unit, _ = _FILTERS[name]
        match = _VALUE.fullmatch(value)
        if match is None:
            raise ValueError(
                f"Invalid value in filter {item!r}: expected a whole number, "
                f"optionally followed by {unit!r}, for example "
                f"'{name}:100{unit}'."
            )
        if match["unit"] and match["unit"] != unit:
            raise ValueError(
                f"Wrong unit in filter {item!r}: {name!r} takes {unit!r}, "
                f"not {match['unit']!r}."
            )
        filters.append(f"{name}:{match['number']}{unit}")
    return filters


class TileLayerColorFilter(JSCSSMixin, TileLayer):
    """
    Add a tile layer and apply CSS color filters to its tiles.

    This wraps the `Leaflet.TileLayer.ColorFilter plugin
    <https://github.com/xtk93x/Leaflet.TileLayer.ColorFilter>`_. A CSS filter
    changes how the tiles are painted, so a single light basemap can serve as a
    dark or grayscale background, which avoids a separate dark tile provider.
    The filter is purely presentational: it applies to the tile images, not to
    markers, vector layers or the controls on top of them.

    Parameters
    ----------
    color_filter: str or list of str
        One or more CSS filters, written as ``"<name>:<number><unit>"``, for
        example ``"invert:100%"`` or ``["grayscale:100%", "contrast:110%"]``.
        Supported filters are blur (px), brightness (%), contrast (%),
        grayscale (%), hue-rotate (deg), invert (%), opacity (%), saturate (%)
        and sepia (%), plus the plugin's short names such as ``"inv"`` or
        ``"gray"``. The unit may be left out, it is added for you.
    tiles: str or :class:`xyzservices.TileProvider`, default 'OpenStreetMap'
        Map tileset to use. See :class:`folium.raster_layers.TileLayer`.
    **kwargs
        Other keyword arguments are passed to
        :class:`folium.raster_layers.TileLayer`.

    Examples
    --------
    A dark basemap from the default tiles:

    >>> m = folium.Map()
    >>> folium.plugins.TileLayerColorFilter(
    ...     ["invert:100%", "hue-rotate:180deg", "brightness:95%", "contrast:90%"],
    ...     name="dark",
    ... ).add_to(m)

    See https://github.com/xtk93x/Leaflet.TileLayer.ColorFilter for the plugin.

    """

    default_js = [
        (
            "leaflet_tilelayer_colorfilter",
            "https://cdn.jsdelivr.net/npm/leaflet.tilelayer.colorfilter@2.0.0/dist/leaflet-tilelayer-colorfilter-global.min.js",
        )
    ]

    def __init__(
        self,
        color_filter: str | Sequence[str],
        tiles: str = "OpenStreetMap",
        **kwargs,
    ):
        super().__init__(tiles=tiles, **kwargs)
        self._name = "TileLayerColorFilter"
        self.color_filter = _normalize_color_filter(color_filter)
        self.options["colorFilter"] = self.color_filter
