"""Folium-specific Figure subclass."""

from branca.element import Figure as BrancaFigure


class Figure(BrancaFigure):
    """Figure that supports repeated rendering without duplicating output.

    Branca elements populate ``header``, ``html``, and ``script`` during
    ``render()``. Some folium elements create new child nodes on every render
    call, which causes repeated ``save()`` calls to accumulate duplicate HTML
    and JavaScript. Clearing the rendered sections before each render makes
    output idempotent while preserving static header content from ``__init__``.
    """

    def render(self, **kwargs):
        meta = self.header._children.pop("meta_http", None)
        self.header._children.clear()
        if meta is not None:
            self.header._children["meta_http"] = meta
        self.html._children.clear()
        self.script._children.clear()
        return super().render(**kwargs)
