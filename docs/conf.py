# flake8: noqa
# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

import inspect
import importlib

import sphinx_compas_theme

# -- General configuration ------------------------------------------------

project = "COMPAS"
copyright = "COMPAS Association"
author = "Tom Van Mele"

release = "1.17.5"
version = ".".join(release.split(".")[0:2])

master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
templates_path = sphinx_compas_theme.get_autosummary_templates_path() + ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints", "_notebooks", "**/__temp"]

# pygments_style = "sphinx"
# pygments_dark_style = "monokai"
# show_authors = True
add_module_names = True
language = "en"


# -- Extension configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    # "sphinx.ext.linkcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.autodoc.typehints",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinx_togglebutton",
    "sphinx_remove_toctrees",
    "sphinx_copybutton",
    # "sphinxcontrib.bibtex",
    "numpydoc",
]

# remove_from_toctrees = ["api/generated/*"]

numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = True

# bibtex options

# bibtex_bibfiles = ['refs.bib']

# autodoc options

autodoc_type_aliases = {}

# this does not work properly yet
# autodoc_typehints = "none"
# autodoc_typehints_format = "short"
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

# plot options

plot_include_source = False
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = ["png"]

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

html_theme = "pydata_sphinx_theme"
html_logo = "_static/images/compas_icon_white_48.png"  # relative to parent of conf.py
html_title = "COMPAS docs"
html_favicon = "_static/images/compas.ico"

html_theme_options = {
    # theme structure and layout
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["version-switcher", "navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "navbar_align": "content",
    "article_header_start": ["breadcrumbs"],
    "article_header_end": [],
    "primary_sidebar_end": [
        # "sidebar-ethical-ads"
    ],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "article_footer_items": ["prev-next.html"],
    "show_prev_next": True,
    "content_footer_items": [],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": ["theme-version"],
    # navigation and links
    "external_links": [
        {"name": "Changelog", "url": "https://github.com/compas-dev/compas/releases"},
        {"name": "COMPAS Framework", "url": "https://compas.dev"},
        {"name": "COMPAS Association", "url": "https://compas.dev/association"},
    ],
    "header_links_before_dropdown": 4,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/compas-dev/compas",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Discourse",
            "url": "http://forum.compas-framework.org/",
            "icon": "fa-brands fa-discourse",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/COMPAS/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
    # "icon_links_label": "Quick Links",
    "use_edit_page_button": True,
    # user interface
    "announcement": "This is the documentation for the pre-release of COMPAS 2.0.",
    "switcher": {
        "json_url": "_static/versions.json",  # relative to _static
        "version_match": release,
    },
    "check_switcher": False,
    # content and features
    # theming and style
    "logo": {
        "image_light": "_static/images/compas_icon_white_48.png",  # relative to parent of conf.py
        "image_dark": "_static/images/compas_icon_white_48.png",  # relative to parent of conf.py
        "text": "COMPAS docs",
    },
    "favicons": [
        {
            "rel": "icon",
            "href": "images/compas.ico",  # relative to the static path
        }
    ],
    "navigation_depth": 2,
    "show_nav_level": 1,
    "show_toc_level": 2,
    "pygment_light_style": "default",
    "pygment_dark_style": "monokai",
}

html_sidebars = {
    "**": [
        "sidebar-nav-bs",
        "sidebar-ethical-ads",
    ],
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "compas-dev",
    "github_repo": "compas",
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]
html_css_files = ["compas.css"]
html_extra_path = []
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = False
html_permalinks = False
html_permalinks_icon = ""
html_compact_lists = True
