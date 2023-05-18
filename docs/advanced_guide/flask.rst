Using folium with flask
=======================

A common use case is to use folium in a flask app. There are multiple ways you
can do that. The simplest is to return the maps html representation. If instead
you want to embed a map on an existing page, you can either embed an iframe
or extract the map components and use those.

Below is a script containing examples for all three use cases:

.. literalinclude:: ../examples/flask_example.py
