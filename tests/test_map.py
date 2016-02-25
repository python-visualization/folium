# -*- coding: utf-8 -*-

"""
Folium map Tests
----------------

"""
from __future__ import unicode_literals

from folium.map import Popup  # TODO: Map, Marker, ...


tmpl = """
        <div id="{id}"
                style="width: {width}; height: {height};">
                {text}</div>
""".format


def test_popup_ascii():
    popup = Popup('Some text.')
    _id = list(popup.html._children.keys())[0]
    kw = dict(id=_id,
              width='100.0%',
              height='100.0%',
              text='Some text.')
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())


def test_popup_quotes():
    popup = Popup("Let's try quotes")
    _id = list(popup.html._children.keys())[0]
    kw = dict(id=_id,
              width='100.0%',
              height='100.0%',
              text='Let&#39;s try quotes')
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())


def test_popup_unicode():
    popup = Popup("Ça c'est chouette")
    _id = list(popup.html._children.keys())[0]
    kw = dict(id=_id,
              width='100.0%',
              height='100.0%',
              text="Ça c&#39;est chouette")
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())
