from typing import List, Tuple

from branca.element import CssLink, Element, Figure, JavascriptLink, MacroElement
from jinja2 import Template


class JSCSSMixin(Element):
    """Render links to external Javascript and CSS resources."""

    default_js: List[Tuple[str, str]] = []
    default_css: List[Tuple[str, str]] = []

    def render(self, **kwargs) -> None:
        figure = self.get_root()
        assert isinstance(
            figure, Figure
        ), "You cannot render this Element if it is not in a Figure."

        for name, url in self.default_js:
            figure.header.add_child(JavascriptLink(url), name=name)

        for name, url in self.default_css:
            figure.header.add_child(CssLink(url), name=name)

        super().render(**kwargs)


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
