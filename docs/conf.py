# flake8: noqa
# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

import sys
import os
import inspect
import importlib
import m2r2

import sphinx_compas_theme
from sphinx.ext.napoleon.docstring import NumpyDocstring

sys.path.append(os.path.join(os.path.dirname(__file__), "_ext"))

# patches

current_m2r2_setup = m2r2.setup


def patched_m2r2_setup(app):
    try:
        return current_m2r2_setup(app)
    except (AttributeError):
        app.add_source_suffix(".md", "markdown")
        app.add_source_parser(m2r2.M2RParser)
    return dict(
        version=m2r2.__version__,
        parallel_read_safe=True,
        parallel_write_safe=True,
    )


m2r2.setup = patched_m2r2_setup

# -- General configuration ------------------------------------------------

project = "COMPAS"
copyright = "Block Research Group - ETH Zurich"
author = "Tom Van Mele"

release = "1.17.9"
version = ".".join(release.split(".")[0:2])

master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = sphinx_compas_theme.get_autosummary_templates_path()
exclude_patterns = ["_build", "**.ipynb_checkpoints", "_notebooks", "**/__temp"]

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
    "sphinx.ext.linkcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "matplotlib.sphinxext.plot_directive",
    "m2r2",
    # "nbsphinx",
    "sphinx.ext.autodoc.typehints",
    "tabs",
]

# autodoc options

autodoc_type_aliases = {}

# this does not work properly yet
autodoc_typehints = "none"
autodoc_typehints_format = "short"
autodoc_typehints_description_target = "documented"

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
    "mathutils",
]

autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"

autoclass_content = "class"


def skip(app, what, name, obj, would_skip, options):
    if name.startswith("_"):
        return True
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


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
    "mathutils",
]

# graph options

inheritance_graph_attrs = dict(rankdir="LR", resolution=150)
inheritance_node_attrs = dict(fontsize=8)

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


def parse_other_attributes_section(self, section):
    return self._format_fields("Other Attributes", self._consume_fields())


NumpyDocstring._parse_other_attributes_section = parse_other_attributes_section


# we now patch the parse method to guarantee that the the above methods are
# assigned to the _section dict
def patched_parse(self):
    self._sections["keys"] = self._parse_keys_section
    self._sections["attributes"] = self._parse_attributes_section
    self._sections["class attributes"] = self._parse_class_attributes_section
    self._sections["other attributes"] = self._parse_other_attributes_section
    self._unpatched_parse()


NumpyDocstring._unpatched_parse = NumpyDocstring._parse
NumpyDocstring._parse = patched_parse


# plot options

plot_include_source = False
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ["png"]
# plot_pre_code
# plot_basedir
# plot_rcparams
# plot_apply_rcparams
# plot_working_directory

plot_template = """
{{ only_html }}

   {% for img in images %}
   {% set has_class = false %}

   .. figure:: {{ build_dir }}/{{ img.basename }}.{{ default_fmt }}
      :class: figure-img img-fluid

      {{ caption }}

   {% endfor %}
"""

# intersphinx options

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "compas": ("https://compas.dev/compas/latest/", None),
}

# linkcode


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    if not info["fullname"]:
        return None

    package = info["module"].split(".")[0]
    if not package.startswith("compas"):
        return None

    module = importlib.import_module(info["module"])
    parts = info["fullname"].split(".")

    if len(parts) == 1:
        obj = getattr(module, info["fullname"])
        mod = inspect.getmodule(obj)
        if not mod:
            return None
        filename = mod.__name__.replace(".", "/")
        lineno = inspect.getsourcelines(obj)[1]
    elif len(parts) == 2:
        obj_name, attr_name = parts
        obj = getattr(module, obj_name)
        attr = getattr(obj, attr_name)
        if inspect.isfunction(attr):
            mod = inspect.getmodule(attr)
            if not mod:
                return None
            filename = mod.__name__.replace(".", "/")
            lineno = inspect.getsourcelines(attr)[1]
        else:
            return None
    else:
        return None

    return f"https://github.com/compas-dev/compas/blob/main/src/{filename}.py#L{lineno}"


# extlinks


extlinks = {
    "rhino": ("https://developer.rhino3d.com/api/RhinoCommon/html/T_%s.htm", "%s"),
    "blender": ("https://docs.blender.org/api/2.93/%s.html", "%s"),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "compas"
html_theme_path = sphinx_compas_theme.get_html_theme_path()
html_theme_options = {
    "navbar_active": "compas",
    "package_version": release,
    "package_docs": "https://compas.dev/compas/",
    "package_old_versions_txt": "https://compas.dev/compas/doc_versions.txt",
}
html_context = {}
html_static_path = sphinx_compas_theme.get_html_static_path()
html_extra_path = []
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = False
html_permalinks = False
html_permalinks_icon = ""
html_experimental_html5_writer = False
html_compact_lists = True
