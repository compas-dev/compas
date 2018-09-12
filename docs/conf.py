# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

import sys
import os

# sys.path.append(os.path.abspath('../../sphinx_compas_theme/sphinxext'))
# sys.path.append(os.path.abspath('../temp/sphinx_compas_theme/sphinxext'))

# -- General configuration ------------------------------------------------

project          = 'COMPAS'
copyright        = '2017, Block Research Group - ETH Zurich'
author           = 'Tom Van Mele'
release          = '0.3.2'
version          = '.'.join(release.split('.')[0:2])

master_doc       = 'index'
source_suffix    = ['.rst', ]
templates_path   = ['_templates', ]
exclude_patterns = ['__build', '**.ipynb_checkpoints', '_notebooks']

pygments_style   = 'sphinx'
show_authors     = True
add_module_names = True
language         = None


# -- Extension configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'matplotlib.sphinxext.plot_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    # 'plotfigure',
]

# autodoc options

autodoc_default_flags = [
    'undoc-members',
    'private-members',
    'special-members',
    'show-inheritance',
]

autodoc_member_order = 'alphabetical'

# autosummary options

autosummary_generate = True

# napoleon options

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

# plot options

# plot_include_source
# plot_pre_code
# plot_basedir
# plot_formats
# plot_rcparams
# plot_apply_rcparams
# plot_working_directory

# {% has_class = false -%}
# {% for option in options -%}
# {% if option.startswith(':class:') %}
# {% has_class = true %}
# {% endif %}
# {% endfor %}


plot_template = """
{{ source_code }}

{{ only_html }}

   {% if source_link or (html_show_formats and not multi_image) %}
   (
   {%- if source_link -%}
   `Source code <{{ source_link }}>`__
   {%- endif -%}
   {%- if html_show_formats and not multi_image -%}
     {%- for img in images -%}
       {%- for fmt in img.formats -%}
         {%- if source_link or not loop.first -%}, {% endif -%}
         `{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
       {%- endfor -%}
     {%- endfor -%}
   {%- endif -%}
   )
   {% endif %}

   {% for img in images %}
   {% set has_class = false %}

   .. figure:: {{ build_dir }}/{{ img.basename }}.{{ default_fmt }}
      {% for option in options -%}
      {%- if option.startswith(':class:') -%}
      {%- set has_class = true -%}
      {%- if 'img-fluid' not in option -%}
      {%- set option = option + ' img-fluid' -%}
      {%- endif -%}
      {%- if 'figure-img' not in option -%}
      {%- set option = option + ' figure-img' -%}
      {%- endif -%}
      {%- endif -%}
      {{ option }}
      {% endfor %}
      {%- if not has_class -%}
      :class: figure-img img-fluid
      {%- endif %}

      {% if html_show_formats and multi_image -%}
        (
        {%- for fmt in img.formats -%}
        {%- if not loop.first -%}, {% endif -%}
        `{{ fmt }} <{{ dest_dir }}/{{ img.basename }}.{{ fmt }}>`__
        {%- endfor -%}
        )
      {%- endif -%}

      {{ caption }}
   {% endfor %}

{{ only_latex }}

   {% for img in images %}
   {% if 'pdf' in img.formats -%}
   .. figure:: {{ build_dir }}/{{ img.basename }}.pdf
      {% for option in options -%}
      {{ option }}
      {% endfor %}

      {{ caption }}
   {% endif -%}
   {% endfor %}

{{ only_texinfo }}

   {% for img in images %}
   .. image:: {{ build_dir }}/{{ img.basename }}.png
      {% for option in options -%}
      {{ option }}
      {% endfor %}

   {% endfor %}

"""

plot_html_show_source_link = False
plot_html_show_formats = False

# intersphinx options

intersphinx_mapping = {'python': ('https://docs.python.org/', None)}


# -- Options for HTML output ----------------------------------------------

html_theme = 'compas'
html_theme_path = ['../../sphinx_compas_theme', '../temp/sphinx_compas_theme']
html_theme_options = {
    'navbar_active' : 'main',
}
html_context = {}
html_static_path = []
html_extra_path = ['.nojekyll']
html_last_updated_fmt = ''
html_copy_source = False
html_show_sourcelink = False
html_add_permalinks = ''
html_experimental_html5_writer = True
html_compact_lists = True
