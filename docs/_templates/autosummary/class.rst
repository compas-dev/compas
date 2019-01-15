.. rst-class:: detail

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block attributes %}
    {% if not attributes %}

    .. rubric:: Attributes

    .. autosummary::
    {% for item in attributes %}
    {%- if item not in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

    .. rubric:: Inherited Attributes

    .. autosummary::
    {% for item in attributes %}
    {%- if item in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

    {% endif %}
    {% endblock %}

    {% block methods %}
    {% if methods %}

    .. rubric:: Methods

    .. autosummary::
        :toctree:

    {% for item in methods %}
    {%- if item not in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

    .. rubric:: Inherited Methods

    .. autosummary::
        :toctree:

    {% for item in methods %}
    {%- if item in inherited_members %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}

    {% endif %}
    {% endblock %}
