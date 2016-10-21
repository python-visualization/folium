# -*- coding: utf-8 -*-
"""
Folium Notebooks Tests
----------------------

Here we try to execute all notebooks that are in `folium/examples`.
"""

import os
import sys
import branca.utilities

if sys.version_info[:2] >= (3, 5):
    import nbconvert

    rootpath = os.path.abspath(os.path.dirname(__file__))

    class NotebookTester(object):
        def __init__(self, filename):
            self.filename = filename

        def __call__(self, exporter=None, filename=None):
            raw_nb = nbconvert.exporters.Exporter().from_filename(self.filename)
            raw_nb[0].metadata.setdefault('kernelspec', {})['name'] = 'python'
            exec_nb = nbconvert.preprocessors.ExecutePreprocessor(timeout=600).preprocess(*raw_nb)

            if exporter is not None:
                out_nb = nbconvert.exporters.MarkdownExporter().from_notebook_node(*exec_nb)
                if filename is None:
                    assert self.filename.endswith('.ipynb')
                    filename = self.filename[:-6] + exporter.file_extension
                open(filename, 'w').write(out_nb[0].encode('utf-8'))

    class TestNotebooks(object):
        _filepath = rootpath.rstrip('/') + '/../../examples/'
        _nblist = [x for x in os.listdir(_filepath) if x.endswith('.ipynb')]

    for fn in TestNotebooks._nblist:
                setattr(TestNotebooks,
                        'test_'+branca.utilities._camelify(fn[:-6]),
                        NotebookTester(TestNotebooks._filepath+fn).__call__
                        )
