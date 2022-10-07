"""
Folium map Tests
----------------

"""

import pytest

from folium import Map
from folium.map import Popup, Icon, CustomPane, Marker
from folium.utilities import normalize


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
    var {popup_name} = L.popup({{
        "autoClose": false, "closeOnClick": false, "maxWidth": "100%"
    }});
    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">Some text.</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name});
    """.format(popup_name=popup.get_name(),
               html_name=list(popup.html._children.keys())[0],
               map_name=m.get_name())
    assert normalize(rendered) == normalize(expected)


def test_popup_show():
    m = Map()
    popup = Popup('Some text.', show=True).add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})
    expected = """
    var {popup_name} = L.popup({{
        "autoClose": false, "maxWidth": "100%"
    }});
    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">Some text.</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name}).openPopup();
    """.format(popup_name=popup.get_name(),
               html_name=list(popup.html._children.keys())[0],
               map_name=m.get_name())
    # assert compare_rendered(rendered, expected)
    assert normalize(rendered) == normalize(expected)


def test_icon_valid_marker_colors():
    assert len(Icon.color_options) == 19
    with pytest.warns(None) as record:
        for color in Icon.color_options:
            Icon(color=color)
    assert len(record) == 0


def test_custom_pane_show():
    m = Map()
    pane = CustomPane('test-name', z_index=625, pointer_events=False).add_to(m)
    rendered = pane._template.module.script(this=pane, kwargs={})
    expected = """
    var {pane_name} = {map_name}.createPane("test-name");
    {pane_name}.style.zIndex = 625;
    {pane_name}.style.pointerEvents = 'none';
    """.format(pane_name=pane.get_name(),
               map_name=m.get_name())
    assert normalize(rendered) == normalize(expected)


def test_marker_valid_location():
    m = Map()
    marker = Marker()
    marker.add_to(m)
    with pytest.raises(ValueError):
        m.render()


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_icon_invalid_marker_colors():
    pytest.warns(UserWarning, Icon, color='lila')
    pytest.warns(UserWarning, Icon, color=42)
    pytest.warns(UserWarning, Icon, color=None)
