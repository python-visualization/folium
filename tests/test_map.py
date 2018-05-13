# -*- coding: utf-8 -*-

"""
Folium map Tests
----------------

"""

from __future__ import (absolute_import, division, print_function)

from folium import Map
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


def test_popup_sticky():

    m = Map()
    popup = Popup('Some text.', sticky=True).add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})

    expected = """
            var {0} = L.popup({{maxWidth: \'300\'
            , autoClose: false
            , closeOnClick: false}});

            
                var {1} = $(\'<div id="{1}" style="width: 100.0%; height: 100.0%;">Some text.</div>\')[0];
                {0}.setContent({1});
            

            {2}.bindPopup({0});

            
        """.format(popup.get_name(),
           list(popup.html._children.items())[0][0],
           m.get_name())

    assert rendered == expected

    
def test_popup_show():

    m = Map()
    popup = Popup('Some text.', show=True).add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})

    expected = """
            var {0} = L.popup({{maxWidth: \'300\'
            , autoClose: false
            }});

            
                var {1} = $(\'<div id="{1}" style="width: 100.0%; height: 100.0%;">Some text.</div>\')[0];
                {0}.setContent({1});
            

            {2}.bindPopup({0});

            
        """.format(popup.get_name(),
           list(popup.html._children.items())[0][0],
           m.get_name())

    assert rendered == expected
