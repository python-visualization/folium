{% extends 'python.tpl'%}
{% block header -%}
{% endblock header %}
{% block codecell %}{{super().replace('get_ipython', '# get_ipython') if "get_ipython" in super() else super()}}{% endblock codecell %}
{% block markdowncell -%}
{% endblock markdowncell %}