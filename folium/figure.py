"""Folium-specific Figure subclass."""

from branca.element import Figure as BrancaFigure

# Re-export branca Figure for folium maps. Rendering must not clear
# figure.html children that were added directly (e.g. geopandas legends).


class Figure(BrancaFigure):
    """Figure used as the root container for folium maps."""
