Installing
==========

Requirements
------------
::

 jinja2

Though Folium requires only `jinja2` to run, some functionalities may require
`numpy` or `pandas` parameters.


Installation
------------

Easiest
~~~~~~~
::

$pip install folium

Or from the source

$python setup.py install

From Source
~~~~~~~~~~~
Choose the sandbox folder of your choice (`~/sandbox` for example)
::

$ cd ~/sandbox

Clone `folium` from github:
::

$ git clone https://github.com/python-visualization/folium

Run the installation script
::

$ cd folium
$ python setup.py install

Run the tests
-------------

To run the tests, you'll also need to install:
::

 flake8
 pandas
 pytest
 vincent

Then go in folium base folder (`~/sandbox/folium` for example)
::

$ cd ~/sandbox/folium

Run the test
::

$ py.test

Build the docs
--------------

To build the docs, you'll also need to install:
::

 sphinx

Then go in folium base folder (`~/sandbox/folium` for example)
::

$ cd ~/sandbox/folium

Build the docs
::

$ rm -rf docs/_build; sphinx-build -b html docs/ docs/_build/html

Then the documentation is in `docs/_build/html/index.html`.
