# -*- coding: utf-8 -*-
"""
Features
------

A generic class for creating features.
"""
from uuid import uuid4

from jinja2 import Environment, PackageLoader, Template
ENV = Environment(loader=PackageLoader('folium', 'templates'))
from collections import OrderedDict
import json

from .six import text_type, binary_type


class Feature(object):
    """Basic feature object that does nothing.
    Other features may inherit from this one."""
    def __init__(self, template=None, template_name=None):
        """Creates a feature."""
        self._name = 'Feature'
        self._id = uuid4().hex
        self._env = ENV
        self._children = OrderedDict()
        self._parent = None
        self._template = Template(template) if template is not None\
            else ENV.get_template(template_name) if template_name is not None\
            else Template("""
        {% for name, feature in this._children.items() %}
            {{feature.render(**kwargs)}}
        {% endfor %}
        """)

    def add_children(self, child, name=None, index=None):
        """Add a children."""
        if name is None:
            name = text_type(child._name)+u"_"+text_type(child._id)
        if index is None:
            self._children[name] = child
        else:
            items = [item for item in self._children.items() if item[0] <> name]
            items.insert(int(index),(name,child))
            self._children = items
        child._parent = self

    def add_to(self, parent, name=None, index=None):
        """Add feature to a parent."""
        parent.add_children(self, name=name, index=index)

    def to_dict(self, depth=-1, ordered=True):
        if ordered:
            dict_fun = OrderedDict
        else:
            dict_fun = dict
        out = dict_fun()
        out['name'] = self._name
        out['id'] = self._id
        if depth <> 0:
            out['children'] = dict_fun([(name, child.to_dict(depth=depth-1))\
                    for name,child in self._children.items()])
        return out

    def to_json(self, depth=-1, **kwargs):
        return json.dumps(self.to_dict(depth=depth, ordered=True), **kwargs)

    def get_root(self):
        """Returns the root of the features tree."""
        if self._parent is None:
            return self
        else:
            return self._parent.get_root()

    def render(self, **kwargs):
        """TODO : docstring here."""
        return self._template.render(this=self, kwargs=kwargs)

class Figure(Feature):
    def __init__(self):
        super(Figure, self).__init__()
        self._name = 'Figure'
        self.header = Feature()
        self.body   = Feature()
        self.script = Feature()

        self.header._parent = self
        self.body._parent = self
        self.script._parent = self

        self._template = Template("""
        <!DOCTYPE html>
        <head>
            {{this.header.render(**kwargs)}}
        </head>
        <body>
            {{this.body.render(**kwargs)}}
        </body>
        <script>
            {{this.script.render(**kwargs)}}
        </script>
        """)
