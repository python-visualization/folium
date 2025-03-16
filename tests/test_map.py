"""
Folium map Tests
----------------

"""

import warnings

import numpy as np
import pytest

from folium import GeoJson, Map, TileLayer
from folium.map import CustomPane, Icon, LayerControl, Marker, Popup
from folium.utilities import normalize

tmpl = """
        <div id="{id}"
                style="width: {width}; height: {height};">
                {text}</div>
""".format


def test_layer_control_initialization():
    layer_control = LayerControl()
    assert layer_control._name == "LayerControl"
    assert layer_control.options["position"] == "topright"
    assert layer_control.options["collapsed"] is True
    assert layer_control.options["autoZIndex"] is True
    assert layer_control.draggable is False
    assert layer_control.base_layers == {}
    assert layer_control.overlays == {}


def test_layer_control_reset():
    layer_control = LayerControl()
    layer_control.base_layers = {"Layer1": "layer1"}
    layer_control.overlays = {"Layer2": "layer2"}
    layer_control.reset()
    assert layer_control.base_layers == {}
    assert layer_control.overlays == {}


def test_layer_control_render():
    m = Map(tiles=None)
    layer1 = TileLayer().add_to(m)
    layer2 = Marker([0, 0]).add_to(m)
    layer3 = GeoJson({}).add_to(m)
    layer1.control = True
    layer2.control = False
    layer3.control = True
    layer1.layer_name = "Layer1"
    layer2.layer_name = "Layer2"
    layer3.layer_name = "Layer3"
    layer1.get_name = lambda: "layer1"
    layer2.get_name = lambda: "layer2"
    layer3.get_name = lambda: "layer3"

    layer_control = LayerControl().add_to(m)
    layer_control.render()

    assert layer_control.base_layers == {"Layer1": "layer1"}
    assert layer_control.overlays == {"Layer3": "layer3"}


def test_layer_control_draggable():
    m = Map(tiles=None)
    layer_control = LayerControl(draggable=True).add_to(m)
    expected = f"new L.Draggable({ layer_control.get_name() }.getContainer()).enable();"
    rendered = m.get_root().render()
    assert normalize(expected) in normalize(rendered)


def test_popup_ascii():
    popup = Popup("Some text.")
    _id = list(popup.html._children.keys())[0]
    kw = {
        "id": _id,
        "width": "100.0%",
        "height": "100.0%",
        "text": "Some text.",
    }
    assert "".join(popup.html.render().split()) == "".join(tmpl(**kw).split())


def test_popup_quotes():
    popup = Popup("Let's try quotes", parse_html=True)
    _id = list(popup.html._children.keys())[0]
    kw = {
        "id": _id,
        "width": "100.0%",
        "height": "100.0%",
        "text": "Let&#39;s try quotes",
    }
    assert "".join(popup.html.render().split()) == "".join(tmpl(**kw).split())


def test_popup_unicode():
    popup = Popup("Ça c'est chouette", parse_html=True)
    _id = list(popup.html._children.keys())[0]
    kw = {
        "id": _id,
        "width": "100.0%",
        "height": "100.0%",
        "text": "Ça c&#39;est chouette",
    }
    assert "".join(popup.html.render().split()) == "".join(tmpl(**kw).split())


def test_popup_sticky():
    m = Map()
    popup = Popup("Some text.", sticky=True).add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})
    expected = """
    var {popup_name} = L.popup({{
        "maxWidth": "100%",
        "autoClose": false,
        "closeOnClick": false,
    }});

    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">Some text.</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name});
    """.format(
        popup_name=popup.get_name(),
        html_name=list(popup.html._children.keys())[0],
        map_name=m.get_name(),
    )
    assert normalize(rendered) == normalize(expected)


def test_popup_show():
    m = Map()
    popup = Popup("Some text.", show=True).add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})
    expected = """
    var {popup_name} = L.popup({{
        "maxWidth": "100%","autoClose": false,
    }});
    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">Some text.</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name}).openPopup();
    """.format(
        popup_name=popup.get_name(),
        html_name=list(popup.html._children.keys())[0],
        map_name=m.get_name(),
    )
    # assert compare_rendered(rendered, expected)
    assert normalize(rendered) == normalize(expected)


def test_popup_backticks():
    m = Map()
    popup = Popup("back`tick`tick").add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})
    expected = """
    var {popup_name} = L.popup({{
        "maxWidth": "100%",
    }});
    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">back\\`tick\\`tick</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name});
    """.format(
        popup_name=popup.get_name(),
        html_name=list(popup.html._children.keys())[0],
        map_name=m.get_name(),
    )
    assert normalize(rendered) == normalize(expected)


def test_popup_backticks_already_escaped():
    m = Map()
    popup = Popup("back\\`tick").add_to(m)
    rendered = popup._template.render(this=popup, kwargs={})
    expected = """
    var {popup_name} = L.popup({{
        "maxWidth": "100%",
    }});
    var {html_name} = $(`<div id="{html_name}" style="width: 100.0%; height: 100.0%;">back\\`tick</div>`)[0];
    {popup_name}.setContent({html_name});
    {map_name}.bindPopup({popup_name});
    """.format(
        popup_name=popup.get_name(),
        html_name=list(popup.html._children.keys())[0],
        map_name=m.get_name(),
    )
    assert normalize(rendered) == normalize(expected)


def test_icon_valid_marker_colors():
    assert len(Icon.color_options) == 19
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        for color in Icon.color_options:
            Icon(color=color)


def test_custom_pane_show():
    m = Map()
    pane = CustomPane("test-name", z_index=625, pointer_events=False).add_to(m)
    rendered = pane._template.module.script(this=pane, kwargs={})
    expected = f"""
    var {pane.get_name()} = {m.get_name()}.createPane("test-name");
    {pane.get_name()}.style.zIndex = 625;
    {pane.get_name()}.style.pointerEvents = 'none';
    """
    assert normalize(rendered) == normalize(expected)


def test_marker_valid_location():
    m = Map()
    marker = Marker()
    marker.add_to(m)
    with pytest.raises(ValueError):
        m.render()


def test_marker_numpy_array_as_location():
    Marker(np.array([0, 0]))


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_icon_invalid_marker_colors():
    pytest.warns(UserWarning, Icon, color="lila")
    pytest.warns(UserWarning, Icon, color=42)
    pytest.warns(UserWarning, Icon, color=None)
