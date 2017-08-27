# -*- coding: utf-8 -*-

"""
Folium map Tests
----------------

"""

from __future__ import (absolute_import, division, print_function)

from folium.map import Popup


tmpl = u"""
        <div id="{id}"
                style="width: {width}; height: {height};">
                {text}</div>
""".format


def test_popup_ascii():
    popup = Popup('Some text.')
    _id = list(popup.html._children.keys())[0]
    kw = {
        'id': _id,
        'width': '100.0%',
        'height': '100.0%',
        'text': 'Some text.',
    }
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())


def test_popup_quotes():
    popup = Popup("Let's try quotes", parse_html=True)
    _id = list(popup.html._children.keys())[0]
    kw = {
        'id': _id,
        'width': '100.0%',
        'height': '100.0%',
        'text': 'Let&#39;s try quotes',
    }
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())


def test_popup_unicode():
    popup = Popup(u"Ça c'est chouette", parse_html=True)
    _id = list(popup.html._children.keys())[0]
    kw = {
        'id': _id,
        'width': '100.0%',
        'height': '100.0%',
        'text': u'Ça c&#39;est chouette',
    }
    assert ''.join(popup.html.render().split()) == ''.join(tmpl(**kw).split())
