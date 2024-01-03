import json
from typing import Union

import jinja2

from folium.utilities import JsCode, TypeJsonValueNoNone, camelize


def tojavascript(obj: Union[str, JsCode, dict]) -> str:
    if isinstance(obj, (str, JsCode)):
        return obj
    elif isinstance(obj, dict):
        out = ["{\n"]
        for key, value in obj.items():
            if value is None:
                continue
            out.append(f'  "{camelize(key)}": ')
            if isinstance(value, JsCode):
                out.append(value)
            else:
                out.append(_to_escaped_json(value))
            out.append(",\n")
        out.append("}")
        return "".join(out)
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")


def _to_escaped_json(obj: TypeJsonValueNoNone) -> str:
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
