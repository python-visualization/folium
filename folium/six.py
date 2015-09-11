import sys
import urllib

PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode
    binary_type = str

if PY3:
    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:
    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))

urlopen = urllib.request.urlopen if PY3 else urllib.urlopen
