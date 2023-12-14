# flake8: noqa
# -*- coding: utf-8 -*-

import sphinx_compas2_theme

# -- General configuration ------------------------------------------------

project = "COMPAS"
copyright = "COMPAS Association"
author = "Tom Van Mele"
organization = "compas-dev"
package = "compas"

master_doc = "index"
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
templates_path = sphinx_compas2_theme.get_autosummary_templates_path()
exclude_patterns = sphinx_compas2_theme.default_exclude_patterns
add_module_names = True
language = "en"

latest_version = sphinx_compas2_theme.get_latest_version()

if latest_version == "Unreleased":
    release = "Unreleased"
    version = "latest"
else:
    release = latest_version
    version = ".".join(release.split(".")[0:2])  # type: ignore

# -- Extension configuration ------------------------------------------------

extensions = sphinx_compas2_theme.default_extensions

# numpydoc options

numpydoc_show_class_members = False
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = True

# bibtex options

# autodoc options

autodoc_type_aliases = {}

autodoc_typehints_description_target = "documented"

autodoc_mock_imports = sphinx_compas2_theme.default_mock_imports

autodoc_default_options = {
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"

autoclass_content = "class"

# autosummary options

autosummary_generate = True
autosummary_mock_imports = sphinx_compas2_theme.default_mock_imports

# graph options

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

linkcode_resolve = sphinx_compas2_theme.get_linkcode_resolve(organization, package)

# extlinks

extlinks = {
    "rhino": ("https://developer.rhino3d.com/api/RhinoCommon/html/T_%s.htm", "%s"),
    "blender": ("https://docs.blender.org/api/2.93/%s.html", "%s"),
}

# from pytorch

from sphinx.writers import html, html5


def replace(Klass):
    old_call = Klass.visit_reference

    def visit_reference(self, node):
        if "refuri" in node:
            refuri = node.get("refuri")
            if "generated" in refuri:
                href_anchor = refuri.split("#")
                if len(href_anchor) > 1:
                    href = href_anchor[0]
                    anchor = href_anchor[1]
                    page = href.split("/")[-1]
                    parts = page.split(".")
                    if parts[-1] == "html":
                        pagename = ".".join(parts[:-1])
                        if anchor == pagename:
                            node["refuri"] = href
        return old_call(self, node)

    Klass.visit_reference = visit_reference


replace(html.HTMLTranslator)
replace(html5.HTML5Translator)

# -- Options for HTML output ----------------------------------------------

html_theme = "multisection"
html_title = project

html_theme_options = {
    "external_links": [
        {"name": "COMPAS Framework", "url": "https://compas.dev"},
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/{organization}/{package}",
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
            "url": f"https://pypi.org/project/{package}/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
    "switcher": {
        "json_url": f"https://raw.githubusercontent.com/{organization}/{package}/gh-pages/versions.json",
        "version_match": version,
    },
    "logo": {
        "image_light": "_static/compas_icon_white.png",  # relative to parent of conf.py
        "image_dark": "_static/compas_icon_white.png",  # relative to parent of conf.py
        "text": "COMPAS docs",
    },
    "anouncements": "This is the WIP documentation for the pre-release of COMPAS 2.0. The documentation of COMPAS 1.x is available <a href='https://compas.dev/compas/stable/'>here</a>.",
    "navigation_depth": 2,
}

html_sidebars = {"index": []}

favicons = [
    {
        "rel": "icon",
        "href": "compas.ico",  # relative to the static path
    }
]

html_context = {
    "github_url": "https://github.com",
    "github_user": organization,
    "github_repo": package,
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = sphinx_compas2_theme.get_html_static_path() + ["_static"]
html_css_files = []
html_extra_path = []
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = True
html_permalinks = False
html_permalinks_icon = ""
html_compact_lists = True
