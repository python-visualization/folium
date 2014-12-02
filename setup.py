# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def walk_subpkg(name):
    data_files = []
    package_dir = 'folium'
    for parent, dirs, files in os.walk(os.path.join(package_dir, name)):
        sub_dir = os.sep.join(parent.split(os.sep)[1:]) # remove package_dir from the path
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
    version='0.1.3',
    description='Make beautiful maps with Leaflet.js & Python',
    author='Rob Story',
    author_email='wrobstory@gmail.com',
    license='MIT License',
    url='https://github.com/wrobstory/folium',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License'],
    packages=['folium'],
    package_data=pkg_data
)
