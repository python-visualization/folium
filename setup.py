# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import re
import sys
import codecs
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

rootpath = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(rootpath, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def walk_subpkg(name):
    data_files = []
    package_dir = 'folium'
    for parent, dirs, files in os.walk(os.path.join(package_dir, name)):
        # Remove package_dir from the path.
        sub_dir = os.sep.join(parent.split(os.sep)[1:])
        for f in files:
            data_files.append(os.path.join(sub_dir, f))
    return data_files


pkg_data = {'': ['*.js',
                 'plugins/*.js',
                 'templates/*.html',
                 'templates/*.js',
                 'templates/*.txt'] + walk_subpkg('templates/tiles')}

LICENSE = read('LICENSE.txt')
version = find_version('folium', '__init__.py')
long_description = '{}\n{}'.format(read('README.txt'), read('CHANGES.txt'))

config = dict(name='folium',
              version=version,
              description='Make beautiful maps with Leaflet.js & Python',
              long_description=long_description,
              author='Rob Story',
              author_email='wrobstory@gmail.com',
              license='MIT License',
              url='https://github.com/python-visualization/folium',
              keywords='data visualization',
              classifiers=['Development Status :: 4 - Beta',
                           'Programming Language :: Python :: 2.7',
                           'Programming Language :: Python :: 3.3',
                           'Programming Language :: Python :: 3.4',
                           'License :: OSI Approved :: MIT License'],
              packages=['folium'],
              package_data=pkg_data,
              zip_safe=False)


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("Remember to also tag the version.")
    sys.exit()
elif sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(**config)
