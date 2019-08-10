.. rst-class:: detail

{% if attributes %}
    {% set proper_attributes = [] %}
    {#
    {% for item in attributes %}
        {% if item not in inherited_members %}
            {{ proper_attributes.append(item) or '' }}
        {% endif %}
    {% endfor %}
    #}
    {% set inherited_attributes = [] %}
    {#
    {% for item in attributes %}
        {% if item in inherited_members %}
            {{ inherited_attributes.append(item) or '' }}
        {% endif %}
    {% endfor %}
    #}
{% endif %}

{% if methods %}
    {% set proper_methods = [] %}
    {% for item in methods %}
        {% if item not in inherited_members %}
            {{ proper_methods.append(item) or '' }}
        {% endif %}
    {% endfor %}
    {% set inherited_methods = [] %}
    {% for item in methods %}
        {% if item in inherited_members %}
            {{ inherited_methods.append(item) or '' }}
        {% endif %}
    {% endfor %}
{% endif %}

{{ objname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block attributes %}
    {% if proper_attributes %}

    .. rubric:: Attributes

    .. autosummary::
    {% for item in proper_attributes %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% if inherited_attributes %}
    .. rubric:: Inherited Attributes

    .. autosummary::
    {% for item in inherited_attributes %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block methods %}
    {% if proper_methods %}
    .. rubric:: Methods

    .. autosummary::
        :toctree:

    {% for item in proper_methods %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}

    {% if inherited %}
    .. rubric:: Inherited Methods

    .. autosummary::
        :toctree:

    {% for item in inherited %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
