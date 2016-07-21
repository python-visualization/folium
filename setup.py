# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

rootpath = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.verbose = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


def extract_version(module='folium'):
    version = None
    fname = os.path.join(rootpath, module, '__init__.py')
    with open(fname) as f:
        for line in f:
            if (line.startswith('__version__')):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters.
                break
    return version


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
                 'plugins/*.html',
                 'plugins/*.css',
                 'plugins/*.tpl',
                 'templates/*.html',
                 'templates/*.js',
                 'templates/*.txt'] + walk_subpkg('templates/tiles')}
pkgs = ['folium',
        'folium.plugins']

LICENSE = read('LICENSE.txt')
long_description = '{}\n{}'.format(read('README.rst'), read('CHANGES.txt'))

# Dependencies.
with open('requirements.txt') as f:
    tests_require = f.readlines()
install_requires = [t.strip() for t in tests_require]


config = dict(name='folium',
              version=extract_version(),
              description='Make beautiful maps with Leaflet.js & Python',
              long_description=long_description,
              author='Rob Story',
              author_email='wrobstory@gmail.com',
              url='https://github.com/python-visualization/folium',
              keywords='data visualization',
              classifiers=['Programming Language :: Python :: 2.7',
                           'Programming Language :: Python :: 3.3',
                           'Programming Language :: Python :: 3.4',
                           'Programming Language :: Python :: 3.5',
                           'Topic :: Scientific/Engineering :: GIS',
                           'Topic :: Scientific/Engineering :: Visualization',
                           'License :: OSI Approved :: MIT License',
                           'Development Status :: 5 - Production/Stable'],
              packages=pkgs,
              package_data=pkg_data,
              cmdclass=dict(test=PyTest),
              tests_require=['pytest'],
              license=LICENSE,
              install_requires=install_requires,
              zip_safe=False)


setup(**config)
