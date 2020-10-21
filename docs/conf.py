# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

import sys
import os

from sphinx.ext.napoleon.docstring import NumpyDocstring

import sphinx_compas_theme

sys.path.insert(0, os.path.abspath("../src"))

# -- General configuration ------------------------------------------------

project = "COMPAS"
copyright = "Block Research Group - ETH Zurich"
author = "Tom Van Mele"

release = "release = '0.16.9'"
version = ".".join(release.split(".")[0:2])

master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = ["_templates", ]
exclude_patterns = ["_build", "**.ipynb_checkpoints", "_notebooks"]

pygments_style = "sphinx"
show_authors = True
add_module_names = True
language = None


# -- Extension configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "matplotlib.sphinxext.plot_directive",
    "m2r",
    "nbsphinx",
]

# autodoc options

autodoc_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils"
]

autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"

autoclass_content = "class"

# autosummary options

autosummary_generate = True
autosummary_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils"
]

# napoleon options

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False


# first, we define new methods for any new sections and add them to the class
def parse_keys_section(self, section):
    return self._format_fields("Keys", self._consume_fields())


NumpyDocstring._parse_keys_section = parse_keys_section


def parse_attributes_section(self, section):
    return self._format_fields("Attributes", self._consume_fields())


NumpyDocstring._parse_attributes_section = parse_attributes_section


def parse_class_attributes_section(self, section):
    return self._format_fields("Class Attributes", self._consume_fields())


NumpyDocstring._parse_class_attributes_section = parse_class_attributes_section


# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections["keys"] = self._parse_keys_section
    self._sections["class attributes"] = self._parse_class_attributes_section
    self._unpatched_parse()


NumpyDocstring._unpatched_parse = NumpyDocstring._parse
NumpyDocstring._parse = patched_parse


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
# {% if option.startswith(":class:") %}
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
      {%- if option.startswith(":class:") -%}
      {%- set has_class = true -%}
      {%- if "img-fluid" not in option -%}
      {%- set option = option + " img-fluid" -%}
      {%- endif -%}
      {%- if "figure-img" not in option -%}
      {%- set option = option + " figure-img" -%}
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
   {% if "pdf" in img.formats -%}
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

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "compas": ("https://compas-dev.github.io/compas", "https://compas-dev.github.io/compas/objects.inv"),
}


# -- Options for HTML output ----------------------------------------------

package_docs_root = "/compas/"

with open(os.path.join(os.path.dirname(__file__), "docversions.txt"), "r") as f:
    version_names = [version.strip() for version in f.readlines()]
    package_docs_versions = [(version, "{}{}".format(package_docs_root, version))
                             for version in version_names if version]

html_theme = "compas"
html_theme_path = sphinx_compas_theme.get_html_theme_path()
html_theme_options = {
    "navbar_active": "compas",
    "package_old_versions": package_docs_versions
}
html_context = {}
html_static_path = []
html_extra_path = [".nojekyll"]
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = False
html_add_permalinks = ""
html_experimental_html5_writer = True
html_compact_lists = True
