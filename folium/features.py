# -*- coding: utf-8 -*-
"""
Features
------

A generic class for creating features.
"""
from uuid import uuid4

from jinja2 import Environment, PackageLoader
ENV = Environment(loader=PackageLoader('folium', 'templates'))
from collections import OrderedDict

class Feature(object):
    """Basic feature object that does nothing.
    Other features may inherit from this one."""
    def __init__(self):
        """Creates a feature."""
        self._name = 'Feature'
        self._id = uuid4().hex
        self._env = ENV
        self._children = []
        self._parent = None

    def add_children(self, child, index=None):
        """Add a children."""
        if index is None:
            self._children.append(child)
        else:
            self._children.insert(int(index),child)
        child._parent = self
        
    def add_to(self, parent, index=None):
        """Add feature to a parent."""
        parent.add_children(self, index=index)

    def render(self, **kwargs):
        """TODO : docstring here."""
        return ""
