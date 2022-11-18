from branca.element import CssLink, Element, Figure, JavascriptLink


class JSCSSMixin(Element):
    """Render links to external Javascript and CSS resources."""

    default_js = []
    default_css = []

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
