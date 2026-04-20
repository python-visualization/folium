import jinja2

from folium.utilities import tojavascript


class Environment(jinja2.Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["tojavascript"] = tojavascript


class Template(jinja2.Template):
    environment_class = Environment
