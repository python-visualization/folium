import json
from typing import Union

import jinja2
from branca.element import Element

from folium.utilities import JsCode, TypeJsonValue, camelize


def tojavascript(obj: Union[str, JsCode, dict, list, Element]) -> str:
    if isinstance(obj, JsCode):
        return obj.js_code
    elif isinstance(obj, Element):
        return obj.get_name()
    elif isinstance(obj, dict):
        out = ["{\n"]
        for key, value in obj.items():
            out.append(f'  "{camelize(key)}": ')
            out.append(tojavascript(value))
            out.append(",\n")
        out.append("}")
        return "".join(out)
    elif isinstance(obj, list):
        out = ["[\n"]
        for value in obj:
            out.append(tojavascript(value))
            out.append(",\n")
        out.append("]")
        return "".join(out)
    else:
        return _to_escaped_json(obj)


def _to_escaped_json(obj: TypeJsonValue) -> str:
    return (
        json.dumps(obj)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("'", "\\u0027")
    )


class Environment(jinja2.Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["tojavascript"] = tojavascript


class Template(jinja2.Template):
    environment_class = Environment
