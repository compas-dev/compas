.. rst-class:: detail

{% set proper_methods = [] %}
{% set inherited_methods = [] %}

{% for item in methods %}
{% if item in inherited_members %}
{% set result = inherited_methods.append(item) %}
{% else %}
{% set result = proper_methods.append(item) %}
{% endif %}
{% endfor %}

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block methods %}

    {% if proper_methods %}
    .. rubric:: Methods

    .. autosummary::
        :toctree:

    {% for item in proper_methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% if inherited_methods %}
    .. rubric:: Inherited Methods

    .. autosummary::
        :toctree:

    {% for item in inherited_methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% endblock %}
