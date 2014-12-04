# -*- coding: utf-8 -*-
import os

import re
VERSIONFILE = "folium/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def walk_subpkg(name):
    data_files = []
    package_dir = 'folium'
    for parent, dirs, files in os.walk(os.path.join(package_dir, name)):
        # Remove package_dir from the path.
        sub_dir = os.sep.join(parent.split(os.sep)[1:])
        for f in files:
            data_files.append(os.path.join(sub_dir, f))
    return data_files

pkg_data = {
    '': ['*.js',
         'plugins/*.js',
         'templates/*.html',
         'templates/*.js',
         'templates/*.txt'] + walk_subpkg('templates/tiles')
}

setup(
    name='folium',
    version=verstr,
    description='Make beautiful maps with Leaflet.js & Python',
    author='Rob Story',
    author_email='wrobstory@gmail.com',
    license='MIT License',
    url='https://github.com/wrobstory/folium',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'License :: OSI Approved :: MIT License'],
    packages=['folium'],
    package_data=pkg_data
)
