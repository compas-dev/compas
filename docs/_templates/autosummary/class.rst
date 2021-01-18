.. rst-class:: detail

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block methods %}

    {% if methods %}
    .. rubric:: Methods

    .. autosummary::
        :toctree:

    {% for item in methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% endblock %}
