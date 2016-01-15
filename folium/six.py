import sys

PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode  # noqa
    binary_type = str

if PY3:
    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:
    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))

if PY3:
    import urllib.request
    urlopen = urllib.request.urlopen
else:
    import urllib
    urlopen = urllib.urlopen
