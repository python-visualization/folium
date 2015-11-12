# -*- coding: utf-8 -*-
"""
Elements
------

A generic class for creating Elements.
"""
from uuid import uuid4

from jinja2 import Environment, PackageLoader, Template
from collections import OrderedDict
import json
import base64

from .six import urlopen, text_type, binary_type
from .utilities import _camelify, _parse_size


ENV = Environment(loader=PackageLoader('folium', 'templates'))


class Element(object):
    """Basic Element object that does nothing.
    Other Elements may inherit from this one."""
    def __init__(self, template=None, template_name=None):
        """Creates a Element."""
        self._name = 'Element'
        self._id = uuid4().hex
        self._env = ENV
        self._children = OrderedDict()
        self._parent = None
        self._template = Template(template) if template is not None\
            else ENV.get_template(template_name) if template_name is not None\
            else Template(u"""
        {% for name, element in this._children.items() %}
            {{element.render(**kwargs)}}
        {% endfor %}
        """)

    def get_name(self):
        return _camelify(self._name) + '_' + self._id

    def add_children(self, child, name=None, index=None):
        """Add a children."""
        if name is None:
            name = child.get_name()
        if index is None:
            self._children[name] = child
        else:
            items = [item for item in self._children.items()
                     if item[0] != name]
            items.insert(int(index), (name, child))
            self._children = items
        child._parent = self

    def add_to(self, parent, name=None, index=None):
        """Add element to a parent."""
        parent.add_children(self, name=name, index=index)

    def to_dict(self, depth=-1, ordered=True, **kwargs):
        if ordered:
            dict_fun = OrderedDict
        else:
            dict_fun = dict
        out = dict_fun()
        out['name'] = self._name
        out['id'] = self._id
        if depth != 0:
            out['children'] = dict_fun([(name, child.to_dict(depth=depth-1))
                                        for name, child in self._children.items()])
        return out

    def to_json(self, depth=-1, **kwargs):
        return json.dumps(self.to_dict(depth=depth, ordered=True), **kwargs)

    def get_root(self):
        """Returns the root of the elements tree."""
        if self._parent is None:
            return self
        else:
            return self._parent.get_root()

    def render(self, **kwargs):
        """TODO : docstring here."""
        return self._template.render(this=self, kwargs=kwargs)

    def save(self, outfile, close_file=True, **kwargs):
        """Saves an Element into a file.

        Parameters
        ----------
        outfile : str or file object
            The file (or filename) where you want to output the html.
        close_file : bool, default True
            Whether the file has to be closed after write.
        """
        if isinstance(outfile, text_type) or isinstance(outfile, binary_type):
            fid = open(outfile, 'wb')
        else:
            fid = outfile

        root = self.get_root()
        html = root.render(**kwargs)
        fid.write(html.encode('utf8'))
        if close_file:
            fid.close()


class Link(Element):
    def get_code(self):
        if self.code is None:
            self.code = urlopen(self.url).read()
        return self.code

    def to_dict(self, depth=-1, **kwargs):
        out = super(Link, self).to_dict(depth=-1, **kwargs)
        out['url'] = self.url
        return out


class JavascriptLink(Link):
    def __init__(self, url, download=False):
        """Create a JavascriptLink object based on a url.
        Parameters
        ----------
            url : str
                The url to be linked
            download : bool, default False
                Whether the target document shall be loaded right now.
        """
        super(JavascriptLink, self).__init__()
        self._name = 'JavascriptLink'
        self.url = url
        self.code = None
        if download:
            self.get_code()

        self._template = Template(u"""
        {% if kwargs.get("embedded",False) %}
            <script>{{this.get_code()}}</script>
        {% else %}
            <script src="{{this.url}}"></script>
        {% endif %}
        """)


class CssLink(Link):
    def __init__(self, url, download=False):
        """Create a CssLink object based on a url.
        Parameters
        ----------
            url : str
                The url to be linked
            download : bool, default False
                Whether the target document shall be loaded right now.
        """
        super(CssLink, self).__init__()
        self._name = 'CssLink'
        self.url = url
        self.code = None
        if download:
            self.get_code()

        self._template = Template(u"""
        {% if kwargs.get("embedded",False) %}
            <style>{{this.get_code()}}</style>
        {% else %}
            <link rel="stylesheet" href="{{this.url}}" />
        {% endif %}
        """)

_default_js = [
    ('leaflet',
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"),
    ('jquery',
     "https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"),
    ('bootstrap',
     "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"),
    ('awesome_markers',
     "https://rawgithub.com/lvoogdt/Leaflet.awesome-markers/2.0/develop/dist/leaflet.awesome-markers.js"),
    ('marker_cluster_src',
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster-src.js"),
    ('marker_cluster',
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"),
    ]

_default_css = [
    ("leaflet_css",
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css"),
    ("bootstrap_css",
     "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"),
    ("bootstrap_theme_css",
     "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"),
    ("awesome_markers_font_css",
     "https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css"),
    ("awesome_markers_css",
     "https://rawgit.com/lvoogdt/Leaflet.awesome-markers/2.0/develop/dist/leaflet.awesome-markers.css"),
    ("marker_cluster_default_css",
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css"),
    ("marker_cluster_css",
     "https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css"),
    ("awesome_rotate_css",
     "https://raw.githubusercontent.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css"),
    ]


class Figure(Element):
    def __init__(self, width="100%", height=None, ratio="60%", figsize=None):
        """Create a Figure object, to plot things into it.

        Parameters
        ----------
            width : str, default "100%"
                The width of the Figure. It may be a percentage or a distance (like "300px").
            height : str, default None
                The height of the Figure. It may be a percentage or a distance (like "300px").
            ratio : str, default "60%"
                A percentage defining the aspect ratio of the Figure.
                It will be ignored if height is not None.
            figsize : tuple of two int, default None
                If you're a matplotlib addict, you can overwrite width and height.
                Values will be converted into pixels in using 60 dpi.
                For example figsize=(10,5) wil result in width="600px", height="300px".
        """
        super(Figure, self).__init__()
        self._name = 'Figure'
        self.header = Element()
        self.html = Element()
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        self.width = width
        self.height = height
        self.ratio = ratio
        if figsize is not None:
            self.width = str(60*figsize[0])+'px'
            self.height = str(60*figsize[1])+'px'

        self._template = Template(u"""
        <!DOCTYPE html>
        <head>
            {{this.header.render(**kwargs)}}
        </head>
        <body>
            {{this.html.render(**kwargs)}}
        </body>
        <script>
            {{this.script.render(**kwargs)}}
        </script>
        """)

        # Create the meta tag
        self.header.add_children(Element(
            '<meta http-equiv="content-type" content="text/html; charset=UTF-8" />'),
            name='meta_http')

        # Import Javascripts
        for name, url in _default_js:
            self.header.add_children(JavascriptLink(url), name=name)

        # Import Css
        for name, url in _default_css:
            self.header.add_children(CssLink(url), name=name)

        self.header.add_children(Element("""
            <style>

            html, body {
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
                }

            #map {
                position:absolute;
                top:0;
                bottom:0;
                right:0;
                left:0;
                }
            </style>
            """), name='css_style')

    def to_dict(self, depth=-1, **kwargs):
        out = super(Figure, self).to_dict(depth=depth, **kwargs)
        out['header'] = self.header.to_dict(depth=depth-1, **kwargs)
        out['html'] = self.html.to_dict(depth=depth-1, **kwargs)
        out['script'] = self.script.to_dict(depth=depth-1, **kwargs)
        return out

    def render(self, **kwargs):
        """TODO : docstring here."""
        for name, child in self._children.items():
            child.render(**kwargs)
        return self._template.render(this=self, kwargs=kwargs)

    def _repr_html_(self, **kwargs):
        """Displays the Figure in a Jupyter notebook.

        Parameters
        ----------
        """
        html = self.render(**kwargs)
        html = "data:text/html;base64," + base64.b64encode(html.encode('utf8')).decode('utf8')

        if self.height is None:
            iframe = """
            <div style="width:{width};">
            <div style="position:relative;width:100%;height:0;padding-bottom:{ratio};">
            <iframe src="{html}" style="position:absolute;width:100%;height:100%;left:0;top:0;">
            </iframe>
            </div></div>""".format(
                html=html,
                width=self.width,
                ratio=self.ratio,
                )
        else:
            iframe = ('<iframe src="{html}" width="{width}" '
                      'height="{height}"></iframe>').format
            iframe = iframe(html=html, width=self.width, height=self.height)
        return iframe

    def add_subplot(self, x, y, n, margin=0.05):
        width = 1./y
        height = 1./x
        left = ((n-1) % y)*width
        top = ((n-1)//y)*height

        left = left+width*margin
        top = top+height*margin
        width = width*(1-2.*margin)
        height = height*(1-2.*margin)

        div = Div(position='absolute',
                  width="{}%".format(100.*width),
                  height="{}%".format(100.*height),
                  left="{}%".format(100.*left),
                  top="{}%".format(100.*top),
                  )
        self.add_children(div)
        return div


class Html(Element):
    def __init__(self, data, width="100%", height="100%"):
        """TODO : docstring here"""
        super(Html, self).__init__()
        self._name = 'Html'
        self.data = data

        self.width = _parse_size(width)
        self.height = _parse_size(height)

        self._template = Template(u"""
        <div id="{{this.get_name()}}"
                style="width: {{this.width[0]}}{{this.width[1]}}; height: {{this.height[0]}}{{this.height[1]}};">
                {{this.data}}</div>
                """)


class Div(Figure):
    def __init__(self, width='100%', height='100%',
                 left="0%", top="0%", position='relative'):
        """Create a Map with Folium and Leaflet.js."""
        super(Figure, self).__init__()
        self._name = 'Div'

        # Size Parameters.
        self.width = _parse_size(width)
        self.height = _parse_size(height)
        self.left = _parse_size(left)
        self.top = _parse_size(top)
        self.position = position

        self.header = Element()
        self.html = Element("""
        {% for name, element in this._children.items() %}
            {{element.render(**kwargs)}}
        {% endfor %}
        """)
        self.script = Element()

        self.header._parent = self
        self.html._parent = self
        self.script._parent = self

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                position : {{this.position}};
                width : {{this.width[0]}}{{this.width[1]}};
                height: {{this.height[0]}}{{this.height[1]}};
                left: {{this.left[0]}}{{this.left[1]}};
                top: {{this.top[0]}}{{this.top[1]}};
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}">
                {{this.html.render(**kwargs)}}
            </div>
        {% endmacro %}
        """)

    def get_root(self):
        return self

    def render(self, **kwargs):
        """TODO : docstring here."""
        figure = self._parent
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        for name, element in self._children.items():
            element.render(**kwargs)

        for name, element in self.header._children.items():
            figure.header.add_children(element, name=name)

        for name, element in self.script._children.items():
            figure.script.add_children(element, name=name)

        header = self._template.module.__dict__.get('header', None)
        if header is not None:
            figure.header.add_children(Element(header(self, kwargs)),
                                       name=self.get_name())

        html = self._template.module.__dict__.get('html', None)
        if html is not None:
            figure.html.add_children(Element(html(self, kwargs)),
                                     name=self.get_name())

        script = self._template.module.__dict__.get('script', None)
        if script is not None:
            figure.script.add_children(Element(script(self, kwargs)),
                                       name=self.get_name())

    def _repr_html_(self, **kwargs):
        """Displays the Div in a Jupyter notebook."""
        if self._parent is None:
            self.add_to(Figure())
            out = self._parent._repr_html_(**kwargs)
            self._parent = None
        else:
            out = self._parent._repr_html_(**kwargs)
        return out


class MacroElement(Element):
    """This is a parent class for Elements defined by a macro template.
    To compute your own element, all you have to do is:
        * To inherit from this class
        * Overwrite the '_name' attribute
        * Overwrite the '_template' attribute with something of the form:
            {% macro header(this, kwargs) %}
                ...
            {% endmacro %}

            {% macro html(this, kwargs) %}
                ...
            {% endmacro %}

            {% macro script(this, kwargs) %}
                ...
            {% endmacro %}
    """
    def __init__(self):
        """TODO : docstring here"""
        super(MacroElement, self).__init__()
        self._name = 'MacroElement'

        self._template = Template(u"")

    def render(self, **kwargs):
        figure = self.get_root()
        assert isinstance(figure, Figure), ("You cannot render this Element "
                                            "if it's not in a Figure.")

        header = self._template.module.__dict__.get('header', None)
        if header is not None:
            figure.header.add_children(Element(header(self, kwargs)),
                                       name=self.get_name())

        html = self._template.module.__dict__.get('html', None)
        if html is not None:
            figure.html.add_children(Element(html(self, kwargs)),
                                     name=self.get_name())

        script = self._template.module.__dict__.get('script', None)
        if script is not None:
            figure.script.add_children(Element(script(self, kwargs)),
                                       name=self.get_name())

        for name, element in self._children.items():
            element.render(**kwargs)
