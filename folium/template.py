import json

import jinja2
import numpy as np
from branca.element import Element

from folium.utilities import JsCode, TypeJsonValue, camelize


def tojavascript(obj: str | JsCode | dict | list | Element) -> str:
    if isinstance(obj, JsCode):
        return obj.js_code
    elif isinstance(obj, Element):
        return obj.get_name()
    elif isinstance(obj, dict):
        out = ["{\n"]
        for key, value in obj.items():
            if isinstance(key, str):
                out.append(f'  "{camelize(key)}": ')
            else:
                out.append(f"  {key}: ")
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


def _json_default(obj):
    """Convert numpy values, which ``json`` can't serialize, to Python ones."""
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _to_escaped_json(obj: TypeJsonValue) -> str:
    return (
        json.dumps(obj, default=_json_default)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("'", "\\u0027")
    )


class Environment(jinja2.Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["tojavascript"] = tojavascript
        self.policies["json.dumps_kwargs"] = {
            **self.policies["json.dumps_kwargs"],
            "default": _json_default,
        }


class Template(jinja2.Template):
    environment_class = Environment
