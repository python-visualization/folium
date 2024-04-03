from branca.element import Element

from folium import JsCode
from folium.template import Environment, Template, _to_escaped_json, tojavascript


def test_tojavascript_with_jscode():
    js_code = JsCode("console.log('Hello, World!')")
    assert tojavascript(js_code) == "console.log('Hello, World!')"


def test_tojavascript_with_element():
    element = Element()
    assert tojavascript(element) == element.get_name()


def test_tojavascript_with_dict():
    dict_obj = {"key": "value"}
    assert tojavascript(dict_obj) == '{\n  "key": "value",\n}'


def test_tojavascript_with_list():
    list_obj = ["value1", "value2"]
    assert tojavascript(list_obj) == '[\n"value1",\n"value2",\n]'


def test_tojavascript_with_string():
    assert tojavascript("Hello, World!") == _to_escaped_json("Hello, World!")


def test_tojavascript_with_combined_elements():
    js_code = JsCode("console.log('Hello, World!')")
    element = Element()
    combined_dict = {
        "key": "value",
        "list": ["value1", "value2", element, js_code],
        "nested_dict": {"nested_key": "nested_value"},
    }
    result = tojavascript(combined_dict)
    expected_lines = [
        "{",
        '  "key": "value",',
        '  "list": [',
        '"value1",',
        '"value2",',
        element.get_name() + ",",
        "console.log('Hello, World!'),",
        "],",
        '  "nestedDict": {',
        '  "nestedKey": "nested_value",',
        "},",
        "}",
    ]
    for result_line, expected_line in zip(result.splitlines(), expected_lines):
        assert result_line == expected_line


def test_to_escaped_json():
    assert _to_escaped_json("hi<>&'") == '"hi\\u003c\\u003e\\u0026\\u0027"'


def test_environment_filter():
    env = Environment()
    assert "tojavascript" in env.filters


def test_template_environment_class():
    assert Template.environment_class == Environment
