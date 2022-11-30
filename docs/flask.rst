Using folium with flask
=======================

A common use case is to use folium in a flask app.
The trick is to return folium's HTML representation.
Here is a simple, complete example on how to return a fullscreen map:


.. literalinclude:: ../examples/flask_example.py


If instead you want to embed a map on an existing page, there are multiple ways
you can go about this.

The easiest is to embed the map in an iframe. You can use a built-in
method to return an iframe:

::

  m = Map()
  iframe = m.get_root()._repr_html()

If you want to customize the iframe width and height:

::

  m.get_root().width = '800px'
  m.get_root().height = '600px'

Alternatively, you can extract the header, html and JS script from the map.
First, render the map. Then, take the pieces. You can then place those on
your own template. Note that the header can contain elements you already
have on your own template. Also, don't forget to make sure Flask doesn't
escape these strings.


::

  m.get_root().render()
  header = m.get_root().header.render()
  body_html = m.get_root().html.render()
  script = m.get_root().script.render()
